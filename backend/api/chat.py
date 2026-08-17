# backend/api/chat.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.schemas import ChatRequest, ChatResponse
import json
import logging
import asyncio

# 引入已初始化好的 RAG 单例
from services.rag_service import rag_system

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", summary="向 AI 厨师提问")
async def chat_with_rag(request: ChatRequest):
    """
    接收用户问题，经过路由分析后调用图 RAG 系统生成回答
    """
    if not rag_system.system_ready:
        raise HTTPException(status_code=503, detail="RAG 系统正在初始化或构建中，请稍后再试。")

    if request.stream:
        # 流式返回 (SSE 格式)
        async def event_generator():
            try:
                # 首先获取路由分析和检索结果 (这部分是同步的，对于生产环境可以包裹在 run_in_executor 中)
                relevant_docs, analysis = rag_system.query_router.route_query(request.query, rag_system.config.top_k)
                
                # 发送路由策略 (可选)
                if request.explain_routing and analysis:
                    strategy_msg = f"💡 [路由策略: {analysis.recommended_strategy.value}]"
                    yield f"data: {json.dumps({'content': strategy_msg + chr(10)}, ensure_ascii=False)}\n\n"
                    await asyncio.sleep(0.05)

                # 调用底层流式生成器
                generator = rag_system.generation_module.generate_adaptive_answer_stream(request.query, relevant_docs)
                
                # 遍历同步生成器并转为异步 yield
                for chunk in generator:
                    if chunk:
                        yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
                        await asyncio.sleep(0.01) # 细微让出协程控制权
                
                yield "data: [DONE]\n\n"
            except Exception as e:
                logger.error(f"流式对话异常: {e}")
                yield f"data: {json.dumps({'content': f'发生内部错误: {str(e)}'}, ensure_ascii=False)}\n\n"
                yield "data: [DONE]\n\n"
            
        return StreamingResponse(event_generator(), media_type="text/event-stream")
    else:
        # 非流式直接返回
        try:
            result, analysis = rag_system.ask_question_with_routing(request.query, stream=False)
            return ChatResponse(
                answer=result,
                strategy=analysis.recommended_strategy.value if analysis else "unknown",
                complexity=analysis.query_complexity if analysis else 0.0
            )
        except Exception as e:
            logger.error(f"非流式对话异常: {e}")
            raise HTTPException(status_code=500, detail=str(e))