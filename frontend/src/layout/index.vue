<!-- src/layout/index.vue -->
<template>
  <div class="dynamic-bg">
    <Sidebar />
    <div class="main-container">
      <HeaderBar />
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from "./components/Sidebar.vue";
import HeaderBar from "./components/HeaderBar.vue";
</script>

<style scoped lang="scss">
.main-container {
  flex: 1;
  margin-left: var(--sidebar-collapsed-width);
  display: flex;
  flex-direction: column;
  position: relative;
}
.main-content {
  margin-top: 40px; /* 留出 HeaderBar 的高度 */
  padding: 30px;
  height: calc(100vh - 40px);
  box-sizing: border-box;
  overflow-y: auto;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
