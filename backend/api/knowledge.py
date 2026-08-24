# backend/api/knowledge.py
from fastapi import APIRouter
from typing import List
from models.schemas import KnowledgeItem
from services.rag_service import rag_system

import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/categories", summary="获取厨房知识分类")
async def get_knowledge_categories():
    # 从图数据库中动态查询已有的知识分类
    categories = ["厨房基本功", "刀工基础", "火候掌握", "食材挑选", "调味秘籍"]
    if rag_system.data_module and rag_system.data_module.driver:
        try:
            with rag_system.data_module.driver.session() as session:
                result = session.run("MATCH (c:Category) RETURN c.name AS name LIMIT 10")
                db_categories = [record["name"] for record in result if record["name"]]
                if db_categories:
                    categories = db_categories
        except Exception as e:
            logger.error(f"查询分类失败: {e}")
            
    return {"categories": categories}

@router.get("/items", response_model=List[KnowledgeItem], summary="获取特定分类下的知识列表")
async def get_knowledge_items(category: str = "厨房基本功", limit: int = 10):
    """从 Neo4j 中获取指定分类的知识/菜谱"""
    items = []
    if rag_system.data_module and rag_system.data_module.driver:
        try:
            with rag_system.data_module.driver.session() as session:
                # 模糊匹配分类，返回相关知识或菜谱
                result = session.run("""
                    MATCH (r:Recipe) 
                    WHERE r.category CONTAINS $category 
                    RETURN r.nodeId AS id, r.name AS title, r.category AS cat, r.content AS content 
                    LIMIT $limit
                """, category=category, limit=limit)
                
                for record in result:
                    content = record["content"] or "暂无详细描述"
                    items.append({
                        "id": record["id"],
                        "title": record["title"],
                        "category": record["cat"] or category,
                        "summary": content[:50] + "...",
                        "content": content
                    })
        except Exception as e:
            logger.error(f"检索知识列表失败: {e}")

    return items