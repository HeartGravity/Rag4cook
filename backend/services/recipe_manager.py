# backend/services/recipe_manager.py
import re
import logging
import os
import uuid
from typing import Tuple, Dict
from fastapi import UploadFile
from langchain_core.docuemnts import Document

# 引入已有的 AI Agent
from agent.recipe_ai_agent import KimiRecipeAgent, RecipeInfo, BailianRecipeAgent
from services.rag_service import rag_system

logger = logging.getLogger(__name__)

class RecipeManager:
    def __init__(self):
        # 从环境变量或配置中读取 API KEY
        # self.kimi_api_key = os.getenv("KIMI_API_KEY", "your_kimi_api_key")
        # self.agent = KimiRecipeAgent(api_key=self.kimi_api_key)
        self.api_key = os.getenv("DASHSCOPE_API_KEY", "")
        self.llm_model = os.getenv("LLM_MODEL", "qwen3.6-flash")
        self.agent = BailianRecipeAgent(api_key=self.api_key, llm_model=self.llm_model)

    def validate_markdown_structure(self, content: str) -> Tuple[bool, str]:
        """
        正则校验 Markdown 是否符合 HowToCook 的标准结构
        """
        required_sections = [
            r"#\s+.+",                     # 必须包含一级标题 (菜名)
            r"##\s+必备原料和工具",          # 必须包含必备原料和工具
            r"##\s+计算",                   # 必须包含计算
            r"##\s+操作"                    # 必须包含操作
        ]
        
        for pattern in required_sections:
            if not re.search(pattern, content):
                return False, f"Markdown 文件缺少必须的章节匹配: {pattern}"
                
        return True, "校验通过"

    async def process_and_import_recipe(self, md_file: UploadFile, category: str, image_url: str = None) -> Dict:
        """
        处理上传的菜谱，调用 Agent 解析，并编排入库
        """
        content_bytes = await md_file.read()
        content = content_bytes.decode('utf-8')
        
        # 1. 结构校验
        is_valid, msg = self.validate_markdown_structure(content)
        if not is_valid:
            raise ValueError(msg)
            
        # 2. 调用 Kimi Agent 提取结构化信息
        logger.info(f"开始使用 Agent 解析菜谱: {md_file.filename}")
        recipe_info: RecipeInfo = self.agent.extract_recipe_info(content, file_path=md_file.filename)
        
        # 如果用户指定了分类，可以覆盖 Agent 提取的分类
        if category:
            recipe_info.category = category

        # 3. 数据入库编排 (此处应该调用 rag_system 或直接写入 Neo4j/Milvus)
        # 示例：构建图节点和向量记录
        recipe_id = f"custom_{uuid.uuid4().hex[:8]}"
        
        # 3.1 写入 Neo4j 图数据库
        if rag_system.data_module and rag_system.data_module.driver:
            with rag_system.data_module.driver.session() as session:
                tags_str = ",".join(recipe_info.tags)
                session.run(
                    """
                    MERGE (r:Recipe {nodeId: $node_id})
                    SET r.name = $name, r.difficulty = $difficulty, 
                        r.category = $category, r.tags = $tags, 
                        r.imageUrl = $image_url, r.content = $content
                    """,
                    node_id=recipe_id, name=recipe_info.name, 
                    difficulty=recipe_info.difficulty, category=recipe_info.category,
                    tags=tags_str, image_url=image_url, content=content[:500]
                )
        else:
            logger.warning("Neo4j 服务未连接，跳过图节点创建")

        # 3.2 写入 Milvus 向量库
        if rag_system.index_module:
            doc = Document(
                page_content=content,
                metadata={
                    "node_id": recipe_id,
                    "recipe_name": recipe_info.name,
                    "node_type": "Recipe",
                    "category": recipe_info.category,
                    "difficulty": recipe_info.difficulty,
                    "doc_type": "recipe"
                }
            )
            # 使用 MilvusIndexConstructionModule 中已有的 add_documents 方法
            success = rag_system.index_module.add_documents([doc])
            if not success:
                logger.error("写入 Milvus 失败")

        logger.info(f"菜谱 {recipe_info.name} 解析与图谱入库完成。")
        
        return {
            "name": recipe_info.name,
            "recipe_id": recipe_id,
            "difficulty": recipe_info.difficulty
        }

recipe_manager = RecipeManager()