import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.rag_service import rag_system

from api import chat, recipe, knowledge

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 生命周期管理：在服务启动时初始化数据库连接和 RAG 引擎
    """
    logger.info("正在初始化后端服务与图 RAG 引擎...")
    rag_system.initialize_system()  # 初始化图 RAG 系统

    if not rag_system.system_ready:
        logger.info("检测到知识库为就绪，开始构建...")
        rag_system.build_knowledge_base()  # 构建知识库

    logger.info("图 RAG 引擎初始化完成，服务准备就绪！")
    yield

    # 服务关闭时清理资源
    logger.info("正在关闭后端服务...")
    rag_system._cleanup()

# 创建 FastAPI 实例
app = FastAPI(
    title="智能烹饪助手 API",
    description="基于 Neo4j + Milvus 的图 RAG 烹饪推荐与问答系统",
    version="1.0.0",
    lifespan=lifespan
)

# 配置 CORS 跨域（允许 Electron 前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议指定具体的前端来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册各个业务路由
app.include_router(chat.router, prefix="/api/chat", tags=["智能问答"])
app.include_router(recipe.router, prefix="/api/recipes", tags=["菜谱管理"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["厨房知识库"])

if __name__ == "__main__":
    import uvicorn
    # 启动服务，默认端口 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)