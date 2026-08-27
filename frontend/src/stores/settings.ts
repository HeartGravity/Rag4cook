// src/stores/settings.ts
import { defineStore } from "pinia";
import { ref } from "vue";

export const useSettingsStore = defineStore("settings", () => {
  // 默认指向本地后端服务
  const apiUrl = ref(localStorage.getItem("apiUrl") || "http://localhost:8000");

  const setApiUrl = (url: string) => {
    apiUrl.value = url;
    localStorage.setItem("apiUrl", url);
  };

  return { apiUrl, setApiUrl };
});
