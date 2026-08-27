// src/api/index.ts
import axios from "axios";
import { useSettingsStore } from "@/stores/settings";

const request = axios.create({
  timeout: 30000,
});

request.interceptors.request.use((config) => {
  const settings = useSettingsStore();
  config.baseURL = settings.apiUrl; // 动态获取 baseURL
  return config;
});

export default request;
