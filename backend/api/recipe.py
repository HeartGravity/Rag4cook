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
                    MATCH (r:Concept {conceptType: 'Recipe'}) 
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
                count_result = session.run("MATCH (r:Concept {conceptType: 'Recipe'}) RETURN count(r) AS total")
                total = count_result.single()["total"]
                
                # 2. 执行分页查询 (SKIP 和 LIMIT)
                skip = (page - 1) * page_size
                result = session.run("""
                    MATCH (r:Concept {conceptType: 'Recipe'})
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

@router.get("/{recipe_id}", summary="获取菜谱详情内容")
@router.get("/detail/{recipe_id}", summary="获取菜谱详情内容")
async def get_recipe_detail(recipe_id: str):
    """
    根据菜谱的 nodeId 从neo4j中获取菜谱的详细数据（包含了关联食材和步骤）
    """
    if not (rag_system.data_module and rag_system.data_module.driver):
        raise HTTPException(status_code=503, detail="数据库未就绪")

    str_recipe_id = str(recipe_id).strip()

    try:
        with rag_system.data_module.driver.session(database="neo4j") as session:
            cypher = """
            MATCH (r:Concept)
            WHERE toString(r.nodeId) = $recipe_id
            
            OPTIONAL MATCH (r)-[req]-(i:Concept)
            WHERE type(req) = 'REQUIRES' OR i.conceptType = 'Ingredient'
            WITH r, collect(DISTINCT CASE WHEN i IS NOT NULL THEN {
                name: i.name,
                amount: COALESCE(req.amount, i.amount, ''),
                unit: COALESCE(req.unit, i.unit, ''),
                category: i.category,
                description: i.description
            } END) AS raw_ingredients
            
            OPTIONAL MATCH (r)-[c]-(s:Concept)
            WHERE type(c) = 'CONTAINS_STEP' OR s.conceptType = 'CookingStep'
            WITH r, raw_ingredients, collect(DISTINCT CASE WHEN s IS NOT NULL THEN {
                name: s.name,
                description: s.description,
                stepNumber: s.stepNumber,
                methods: s.methods,
                tools: s.tools,
                timeEstimate: s.timeEstimate,
                stepOrder: COALESCE(c.stepOrder, s.stepNumber, 999)
            } END) AS raw_steps
            
            RETURN r, 
                   [x IN raw_ingredients WHERE x IS NOT NULL] AS ingredients,
                   [x IN raw_steps WHERE x IS NOT NULL] AS steps
            """
            result = session.run(cypher, recipe_id=str_recipe_id)
            record = result.single()

            if not record or not record["r"]:
                # 兼容自定义上传的 :Recipe 标签节点
                fallback_cypher = "MATCH (r) WHERE toString(r.nodeId) = $recipe_id RETURN r, [] AS ingredients, [] AS steps"
                fallback_res = session.run(fallback_cypher, recipe_id=str_recipe_id)
                record = fallback_res.single()
                if not record or not record["r"]:
                    raise HTTPException(status_code=404, detail="未找到对应的菜谱")

            node = record["r"]
            tags = node.get("tags", "")
            tags_list = tags.split(",") if isinstance(tags, str) and tags else (tags if isinstance(tags, list) else [])

            # 按照步骤对 stepOrder进行升序排序
            steps = record.get("steps", [])
            steps.sort(key=lambda item: item.get("stepOrder", 999))

            return {
                "id": node.get("nodeId"),
                "name": node.get("name"),
                "difficulty": node.get("difficulty") or 3,
                "category": node.get("category") or "",
                "cuisine_type": node.get("cuisineType") or "",
                "prep_time": node.get("prepTime") or "",
                "cook_time": node.get("cookTime") or "",
                "servings": node.get("servings") or "",
                "description": node.get("description") or "",
                "content": node.get("content") or "",
                "tags": tags_list,
                "image_url": node.get("imageUrl"),
                "ingredients": record.get("ingredients", []),
                "steps": steps
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查询菜谱详情失败: {e}")
        raise HTTPException(status_code=500, detail="查询菜谱详情失败")
