// src/stores/favorite.ts
import { defineStore } from "pinia";
import { ref } from "vue";

export interface FavoriteItem {
  id: string;
  name: string;
  type: "recipe" | "knowledge";
  tags?: string[];
}

export const useFavoriteStore = defineStore("favorite", () => {
  const favorites = ref<FavoriteItem[]>(
    JSON.parse(localStorage.getItem("favorites") || "[]"),
  );

  const toggleFavorite = (item: FavoriteItem) => {
    const index = favorites.value.findIndex((f) => f.id === item.id);
    if (index > -1) {
      favorites.value.splice(index, 1); // 取消收藏
    } else {
      favorites.value.push(item); // 加入收藏
    }
    localStorage.setItem("favorites", JSON.stringify(favorites.value));
  };

  const isFavorite = (id: string) => {
    return favorites.value.some((f) => f.id === id);
  };

  return { favorites, toggleFavorite, isFavorite };
});
