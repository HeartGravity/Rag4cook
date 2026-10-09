# backend/api/knowledge.py
from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import KnowledgeItem, KnowledgeListResponse
from services.rag_service import rag_system

import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/categories", summary="获取厨房知识分类")
async def get_knowledge_categories():
    categories = []
    if rag_system.data_module and rag_system.data_module.driver:
        with rag_system.data_module.driver.session(database="neo4j") as session:
            result = session.run("MATCH (c:Concept {conceptType: 'RecipeCategory'}) RETURN c.name as name LIMIT 50")
            categories = [record["name"] for record in result]
    return {"categories": categories}

@router.get("/items", response_model=KnowledgeListResponse, summary="获取特定分类下的知识列表（支持分页）")
async def get_knowledge_items(category: str = "素菜", page: int = 1, page_size: int = 10):
    """
    从 Neo4j 中分页获取指定分类的菜谱，包含用料、难度及智能摘要
    """
    items = []
    total = 0

    if not (rag_system.data_module and rag_system.data_module.driver):
        return {"total": 0, "items": [], "page": page, "page_size": page_size}

    try:
        with rag_system.data_module.driver.session(database="neo4j") as session:
            # 1. 统计该分类下的菜谱总数
            count_query = """
            MATCH (r:Concept {conceptType: 'Recipe'})
            WHERE r.category CONTAINS $category
            RETURN count(r) AS total
            """
            count_res = session.run(count_query, category=category)
            count_record = count_res.single()
            if count_record:
                total = count_record["total"]

            # 2. 分页获取菜谱节点并关联食材（去除 r.content，解决 01N42 告警）
            skip = max(0, (page - 1) * page_size)
            items_query = """
            MATCH (r:Concept {conceptType: 'Recipe'})
            WHERE r.category CONTAINS $category
            WITH r
            ORDER BY r.nodeId
            SKIP $skip LIMIT $limit
            OPTIONAL MATCH (r)-[req]-(i:Concept)
            WHERE type(req) = 'REQUIRES' OR i.conceptType = 'Ingredient'
            WITH r, collect(DISTINCT i.name)[0..5] AS ingredients
            RETURN r.nodeId AS id,
                   r.name AS title,
                   r.category AS cat,
                   r.difficulty AS difficulty,
                   r.description AS description,
                   r.cuisineType AS cuisineType,
                   r.prepTime AS prepTime,
                   r.cookTime AS cookTime,
                   ingredients
            """
            result = session.run(items_query, category=category, skip=skip, limit=page_size)

            for record in result:
                raw_desc = (record["description"] or "").strip()
                ingredients = [name for name in record["ingredients"] if name]
                difficulty = record["difficulty"] or 3

                # 3. 智能构建简要描述，彻底替代原本空白的“暂无详细描述”
                if raw_desc:
                    summary = raw_desc[:80] + ("..." if len(raw_desc) > 80 else "")
                else:
                    summary_parts = []
                    if record["cuisineType"]:
                        summary_parts.append(f"{record['cuisineType']}风味")
                    if record["prepTime"] or record["cookTime"]:
                        time_info = []
                        if record["prepTime"]:
                            time_info.append(f"准备{record['prepTime']}")
                        if record["cookTime"]:
                            time_info.append(f"烹饪{record['cookTime']}")
                        summary_parts.append("，".join(time_info))
                    if ingredients:
                        summary_parts.append(f"主要用料：{', '.join(ingredients[:4])}")

                    if summary_parts:
                        summary = "；".join(summary_parts) + "。"
                    else:
                        summary = f"经典{record['cat'] or '家常'}菜肴，烹饪难度约{difficulty}星，步骤清晰易上手。"

                items.append({
                    "id": str(record["id"]),
                    "title": record["title"],
                    "category": record["cat"] or category,
                    "difficulty": difficulty,
                    "ingredients": ingredients,
                    "summary": summary,
                    "content": raw_desc
                })
    except Exception as e:
        logger.error(f"检索知识列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "total": total,
        "items": items,
        "page": page,
        "page_size": page_size
    }