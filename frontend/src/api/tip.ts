// src/api/tip.ts
import request from "./index";

export interface TipQueryParams {
  category?: string;
  keyword?: string;
  page?: number;
  page_size?: number;
}

export const getTipCategories = () => {
  return request.get("/api/tips/categories");
};

export const getTipItems = (params: TipQueryParams) => {
  return request.get("/api/tips/items", { params });
};

export const getTipDetail = (tipId: string) => {
  return request.get(`/api/tips/${tipId}`);
};
