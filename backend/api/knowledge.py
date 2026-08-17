# backend/api/knowledge.py
from fastapi import APIRouter
from typing import List
from models.schemas import KnowledgeItem

router = APIRouter()

@router.get("/categories", summary="获取厨房知识分类")
async def get_knowledge_categories():
    return {
        "categories": ["厨房基本功", "刀工基础", "火候掌握", "食材挑选", "调味秘籍"]
    }

@router.get("/items", response_model=List[KnowledgeItem], summary="获取特定分类下的知识列表")
async def get_knowledge_items(category: str = "厨房基本功", limit: int = 10):
    # 这里应该从图数据库 (Neo4j) 或 向量库中进行 match
    # 占位返回基本数据结构
    return [
        {
            "id": "k1001",
            "title": "如何正确切洋葱不流泪",
            "category": category,
            "summary": "掌握正确的下刀姿势和冷藏技巧...",
            "content": "洋葱在切之前放入冰箱冷藏15分钟..."
        }
    ]