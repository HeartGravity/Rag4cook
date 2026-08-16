import { contextBridge } from "electron";

// 预留暴露给渲染进程的安全 API 桥梁
contextBridge.exposeInMainWorld("electronAPI", {
  platform: process.platform,
});
