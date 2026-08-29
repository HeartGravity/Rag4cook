<!-- src/layout/components/HeaderBar.vue -->
<template>
  <div class="header-bar">
    <div class="drag-area"></div>
    <div class="window-controls">
      <!-- 这里可以绑定 Electron IPC 通信触发窗口最小化、最大化、关闭 -->
      <div class="control-btn minimize" @click="minimize">
        <el-icon><Minus /></el-icon>
      </div>
      <div class="control-btn maximize" @click="maximize">
        <el-icon><FullScreen /></el-icon>
      </div>
      <div class="control-btn close" @click="closeWindow">
        <el-icon><Close /></el-icon>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Minus, FullScreen, Close } from "@element-plus/icons-vue";

// 假设 Electron preload 中暴露了 windowControls 对象
const minimize = () => window?.electronAPI?.minimize?.();
const maximize = () => window?.electronAPI?.maximize?.();
const closeWindow = () => window?.electronAPI?.close?.();
</script>

<style scoped lang="scss">
.header-bar {
  height: 40px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  position: absolute;
  top: 0;
  left: var(--sidebar-collapsed-width);
  right: 0;
  z-index: 999;
}
/* 核心：设置 Electron 的拖拽区域 */
.drag-area {
  flex: 1;
  -webkit-app-region: drag;
}
.window-controls {
  display: flex;
  -webkit-app-region: no-drag; /* 按钮区域不可拖动 */
}
.control-btn {
  width: 46px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s;
  color: #666;
}
.control-btn:hover {
  background: rgba(0, 0, 0, 0.05);
}
.close:hover {
  background: #f56c6c;
  color: white;
}
</style>
