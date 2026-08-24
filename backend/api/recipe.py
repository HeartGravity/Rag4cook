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
            with rag_system.data_module.driver.session() as session:
                # 随机抽取指定数量的菜谱
                result = session.run("""
                    MATCH (r:Recipe) 
                    WITH r, rand() AS weight 
                    ORDER BY weight 
                    LIMIT $limit 
                    RETURN r.nodeId AS id, r.name AS name, 
                           r.difficulty AS difficulty, r.tags AS tags, r.imageUrl AS image_url
                """, limit=limit)
                
                for record in result:
                    recipes.append({
                        "id": record["id"],
                        "name": record["name"],
                        "difficulty": record["difficulty"] if record["difficulty"] else 3,
                        "tags": record["tags"].split(",") if record["tags"] else ["推荐"],
                        "image_url": record["image_url"]
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