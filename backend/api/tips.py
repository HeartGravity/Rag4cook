# be/api/tips.py
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging
from models.schemas import TipItem, TipListResponse
from services.rag_service import rag_system

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/categories", summary="获取厨房技巧分类及数量")
async def get_tip_categories():
    """从 Neo4j 动态统计 KitchenTip 下的所有细分类别"""
    categories = []
    if not (rag_system.data_module and rag_system.data_module.driver):
        return {"categories": []}

    try:
        with rag_system.data_module.driver.session(database="neo4j") as session:
            cypher = """
            MATCH (t:Concept {conceptType: 'KitchenTip'})
            WHERE t.category IS NOT NULL AND trim(t.category) <> ''
            RETURN DISTINCT t.category AS name, count(t) AS count
            ORDER BY count DESC, name ASC
            """
            result = session.run(cypher)
            for record in result:
                categories.append({
                    "name": record["name"],
                    "count": record["count"]
                })
    except Exception as e:
        logger.error(f"获取技巧分类失败: {e}")
        raise HTTPException(status_code=500, detail="获取技巧分类失败")

    return {"categories": categories}

@router.get("/items", response_model=TipListResponse, summary="分页查询厨房技巧列表")
async def get_tip_items(
    category: Optional[str] = Query(None, description="分类名称"),
    keyword: Optional[str] = Query(None, description="关键词模糊搜索"),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50)
):
    """支持按分类筛选与关键字检索的厨房技巧瀑布流数据接口"""
    if not (rag_system.data_module and rag_system.data_module.driver):
        return {"total": 0, "items": [], "page": page, "page_size": page_size}

    cat_filter = "" if not category or category == "全部" else category
    kw_filter = (keyword or "").strip()
    skip = (page - 1) * page_size

    try:
        with rag_system.data_module.driver.session(database="neo4j") as session:
            # 1. 查询总条数
            count_cypher = """
            MATCH (t:Concept {conceptType: 'KitchenTip'})
            WHERE ($cat = '' OR t.category CONTAINS $cat)
              AND ($kw = '' OR t.name CONTAINS $kw OR coalesce(t.description, '') CONTAINS $kw OR coalesce(t.tags, '') CONTAINS $kw)
            RETURN count(t) AS total
            """
            total_res = session.run(count_cypher, cat=cat_filter, kw=kw_filter)
            total = total_res.single()["total"]

            # 2. 分页查询并关联统计信息
            items_cypher = """
            MATCH (t:Concept {conceptType: 'KitchenTip'})
            WHERE ($cat = '' OR t.category CONTAINS $cat)
              AND ($kw = '' OR t.name CONTAINS $kw OR coalesce(t.description, '') CONTAINS $kw OR coalesce(t.tags, '') CONTAINS $kw)
            WITH t
            ORDER BY t.nodeId DESC
            SKIP $skip LIMIT $limit
            OPTIONAL MATCH (t)-[r]-(related:Concept)
            WITH t, count(DISTINCT related) AS rel_count
            RETURN t.nodeId AS id,
                   t.name AS title,
                   t.category AS category,
                   t.difficulty AS difficulty,
                   t.description AS description,
                   t.methods AS methods,
                   t.tools AS tools,
                   t.safetyWarnings AS safetyWarnings,
                   t.tags AS tags,
                   t.timeEstimate AS timeEstimate,
                   rel_count AS related_count
            """
            result = session.run(items_cypher, cat=cat_filter, kw=kw_filter, skip=skip, limit=page_size)
            
            items = []
            for record in result:
                raw_tags = record["tags"]
                tag_list = raw_tags.split(",") if isinstance(raw_tags, str) and raw_tags else []
                items.append({
                    "id": str(record["id"]),
                    "title": record["title"] or "未知技巧",
                    "category": record["category"] or "综合常识",
                    "difficulty": record["difficulty"] or 1,
                    "description": record["description"] or "",
                    "methods": record["methods"] or "",
                    "tools": record["tools"] or "",
                    "safety_warnings": record["safetyWarnings"] or "",
                    "tags": tag_list,
                    "time_estimate": record["timeEstimate"] or "",
                    "related_count": record["related_count"]
                })

            return {
                "total": total,
                "items": items,
                "page": page,
                "page_size": page_size
            }
    except Exception as e:
        logger.error(f"获取厨房技巧失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{tip_id}", summary="获取特定技巧的详细内容")
async def get_tip_detail(tip_id: str):
    """根据 nodeId 查询单条厨房技巧与关联节点"""
    if not (rag_system.data_module and rag_system.data_module.driver):
        raise HTTPException(status_code=503, detail="数据库未就绪")

    try:
        with rag_system.data_module.driver.session(database="neo4j") as session:
            cypher = """
            MATCH (t:Concept)
            WHERE toString(t.nodeId) = $tip_id
            OPTIONAL MATCH (t)-[r]-(rel:Concept)
            WITH t, collect(DISTINCT CASE WHEN rel IS NOT NULL THEN {
                id: rel.nodeId,
                name: rel.name,
                type: rel.conceptType,
                relation: type(r)
            } END) AS raw_rel
            RETURN t, [x IN raw_rel WHERE x IS NOT NULL] AS related_nodes
            """
            result = session.run(cypher, tip_id=str(tip_id).strip())
            record = result.single()
            if not record or not record["t"]:
                raise HTTPException(status_code=404, detail="未找到该厨房技巧")

            node = record["t"]
            raw_tags = node.get("tags", "")
            tag_list = raw_tags.split(",") if isinstance(raw_tags, str) and raw_tags else []

            return {
                "id": str(node.get("nodeId")),
                "name": node.get("name"),
                "category": node.get("category") or "通用知识",
                "difficulty": node.get("difficulty") or 1,
                "description": node.get("description") or "",
                "methods": node.get("methods") or "",
                "tools": node.get("tools") or "",
                "safety_warnings": node.get("safetyWarnings") or "",
                "time_estimate": node.get("timeEstimate") or "",
                "tags": tag_list,
                "related_nodes": record.get("related_nodes", [])
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查询技巧详情失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))