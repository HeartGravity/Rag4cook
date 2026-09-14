import { contextBridge, ipcRenderer } from "electron";

// 预留暴露给渲染进程的安全 API 桥梁
contextBridge.exposeInMainWorld("electronAPI", {
  platform: process.platform,

  minimize: () => ipcRenderer.send("window-minimize"),
  maximize: () => ipcRenderer.send("window-maximize"),
  close: () => ipcRenderer.send("window-close"),
});
