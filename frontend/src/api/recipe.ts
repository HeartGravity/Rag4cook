// src/api/recipe.ts
import request from "./index";

export const getRecommendRecipes = (limit = 4) => {
  return request.get("/api/recipes/recommend", { params: { limit } });
};

export const getKnowledgeCategories = () => {
  return request.get("/api/knowledge/categories");
};

export const getKnowledgeItems = (category: string, limit = 10) => {
  return request.get("/api/knowledge/items", { params: { category, limit } });
};
