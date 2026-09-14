# backend/api/recipe.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
import logging

from models.schemas import RecipeRecommendResponse, RecipeUploadResponse
from services.storage_service import storage_service
from services.recipe_manager import recipe_manager
from services.rag_service import rag_system

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/recommend", response_model=List[RecipeRecommendResponse], summary="获取首页推荐菜谱")
async def get_recommended_recipes(limit: int = 4):
    """
    通过 Neo4j 获取随机推荐的菜谱列表
    """
    recipes = []
    if rag_system.data_module and rag_system.data_module.driver:
        try:
            with rag_system.data_module.driver.session(database="neo4j") as session:
                # 随机抽取指定数量的菜谱
                result = session.run("""
                    MATCH (r:Concept {contentType: 'Recipe'}) 
                    WITH r, rand() AS weight 
                    ORDER BY weight 
                    LIMIT $limit 
                    RETURN r.nodeId AS id, r.name AS name, 
                           r.difficulty AS difficulty, r.tags AS tags
                """, limit=limit)
                
                for record in result:
                    recipes.append({
                        "id": record["id"],
                        "name": record["name"],
                        "difficulty": record["difficulty"] if record["difficulty"] else 3,
                        "tags": record["tags"].split(",") if record["tags"] else ["推荐"],
                        "image_url": None
                    })
        except Exception as e:
            logger.error(f"查询推荐菜谱失败: {e}")
    
    # 如果数据库中没有数据，提供一点默认保底数据
    if not recipes:
        recipes = [{"id": "fallback_1", "name": "暂无推荐", "difficulty": 3, "tags": [], "image_url": None}]
        
    return recipes

@router.post("/upload", response_model=RecipeUploadResponse, summary="上传新菜谱 (Markdown + 图片)")
async def upload_recipe(
    file: UploadFile = File(..., description="Markdown 菜谱文件"),
    image: UploadFile = File(None, description="菜谱成品图片"),
    category: str = Form(..., description="前端表单传递的分类参数")
):
    """
    处理用户上传的 Markdown 菜谱：
    1. 将图片和文件存入 MinIO
    2. 正则校验 Markdown 结构是否合规并由 Agent 解析入库 (Neo4j + Milvus)
    """
    if not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="必须上传 .md 格式的 Markdown 文件")
    
    try:
        # 1. 保存图片到对象存储
        image_url = None
        if image:
            image_url = await storage_service.upload_file(image, sub_folder="images")

        # 2. 保存 MD 源文件到对象存储 (可选)
        await storage_service.upload_file(file, sub_folder="markdowns")

        # 3. 解析与图谱入库编排
        result_meta = await recipe_manager.process_and_import_recipe(
            md_file=file, 
            category=category, 
            image_url=image_url
        )

        return RecipeUploadResponse(
            message=f"菜谱 {result_meta['name']} 上传解析并入库成功",
            filename=file.filename,
            recipe_id=result_meta['recipe_id'],
            image_url=image_url
        )
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"菜谱上传处理失败: {e}")
        raise HTTPException(status_code=500, detail="内部服务器错误，解析入库失败")

@router.get("/list", summary="获取分页菜谱列表")
async def get_recipe_list(page: int = 1, page_size: int = 10):
    """
    从 Neo4j 数据库获取菜谱列表，支持分页
    """
    recipes = []
    total = 0
    
    # 确保数据库连接就绪
    if rag_system.data_module and rag_system.data_module.driver:
        try:
            with rag_system.data_module.driver.session(database="neo4j") as session:
                # 1. 获取数据库中菜谱的总数量
                count_result = session.run("MATCH (r:Concept {contentType: 'Recipe'}) RETURN count(r) AS total")
                total = count_result.single()["total"]
                
                # 2. 执行分页查询 (SKIP 和 LIMIT)
                skip = (page - 1) * page_size
                result = session.run("""
                    MATCH (r:Concept {contentType: 'Recipe'})
                    RETURN r.nodeId AS id, r.name AS name, 
                           r.category AS category, r.difficulty AS difficulty
                    ORDER BY r.nodeId DESC
                    SKIP $skip LIMIT $limit
                """, skip=skip, limit=page_size)
                
                # 3. 格式化返回数据
                for record in result:
                    recipes.append({
                        "id": record["id"],
                        "name": record["name"],
                        "category": record["category"] or "未分类",
                        "difficulty": record["difficulty"] or 3
                    })
        except Exception as e:
            logger.error(f"查询菜谱列表失败: {e}")
            raise HTTPException(status_code=500, detail="数据库查询失败")
            
    return {
        "total": total,
        "data": recipes,
        "page": page,
        "page_size": page_size
    }