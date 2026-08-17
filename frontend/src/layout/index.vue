<!-- src/layout/index.vue -->
<template>
  <div class="dynamic-bg">
    <!-- 引入侧边栏 -->
    <Sidebar />

    <!-- 主内容区 -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import Sidebar from "./components/Sidebar.vue";
</script>

<style scoped lang="scss">
.main-content {
  flex: 1;
  /* 留出一点左侧感应区的空间 */
  margin-left: var(--sidebar-collapsed-width);
  padding: 30px;
  height: 100vh;
  box-sizing: border-box;
  overflow-y: auto;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
