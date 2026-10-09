// src/api/recipe.ts
import request from "./index";

export const getRecommendRecipes = (limit = 4) => {
  return request.get("/api/recipes/recommend", { params: { limit } });
};

export const getRecipeDetail = (recipeId: string) => {
  return request.get(`/api/recipes/${recipeId}`);
};

export const getKnowledgeCategories = () => {
  return request.get("/api/knowledge/categories");
};

export const getKnowledgeItems = (
  category: string,
  page = 1,
  pageSize = 10,
) => {
  return request.get("/api/knowledge/items", {
    params: { category, page, page_size: pageSize },
  });
};

export const uploadRecipe = (formData: FormData) => {
  return request.post("/api/recipes/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

export const getRecipesList = (page = 1, pageSize = 10) => {
  return request.get("/api/recipes/list", {
    params: { page, page_size: pageSize },
  });
};
