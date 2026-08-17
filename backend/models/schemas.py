# backend/models/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    query: str = Field(..., description="用户的提问内容")
    stream: bool = Field(default=True, description="是否使用流式输出(SSE)")
    explain_routing: bool = Field(default=False, description="是否返回路由分析结果")

class ChatResponse(BaseModel):
    answer: str
    strategy: Optional[str] = None
    complexity: Optional[float] = None

class RecipeRecommendResponse(BaseModel):
    id: str
    name: str
    difficulty: int
    tags: List[str]
    image_url: Optional[str] = None

class RecipeUploadResponse(BaseModel):
    message: str
    filename: str
    recipe_id: Optional[str] = None
    image_url: Optional[str] = None

class KnowledgeItem(BaseModel):
    id: str
    title: str
    category: str
    summary: Optional[str] = None
    content: Optional[str] = None