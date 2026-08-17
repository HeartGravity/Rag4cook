<template>
  <div class="sidebar-wrapper">
    <!-- 侧边栏主体 -->
    <div class="sidebar">
      <div class="logo">
        <el-icon :size="24"><Food /></el-icon>
        <span class="title">尝尝咸淡</span>
      </div>

      <nav class="nav-menu">
        <router-link to="/home" class="nav-item" active-class="active">
          <el-icon><House /></el-icon> <span>首页探索</span>
        </router-link>
        <router-link to="/chat" class="nav-item" active-class="active">
          <el-icon><ChatDotRound /></el-icon> <span>智能问答</span>
        </router-link>
        <router-link to="/knowledge" class="nav-item" active-class="active">
          <el-icon><Reading /></el-icon> <span>菜谱知识库</span>
        </router-link>
        <router-link to="/favorites" class="nav-item" active-class="active">
          <el-icon><Star /></el-icon> <span>我的收藏</span>
        </router-link>
        <router-link to="/manage" class="nav-item" active-class="active">
          <el-icon><Setting /></el-icon> <span>知识管理</span>
        </router-link>
      </nav>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  House,
  ChatDotRound,
  Food,
  Star,
  Setting,
  Reading,
} from "@element-plus/icons-vue";
</script>

<style scoped lang="scss">
.sidebar-wrapper {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  width: var(--sidebar-collapsed-width);
  z-index: 1000;
  transition: width 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);

  /* 悬浮时展开 */
  &:hover {
    width: var(--sidebar-width);

    .sidebar {
      transform: translateX(0);
      box-shadow: 4px 0 15px rgba(0, 0, 0, 0.1);
    }
  }
}

.sidebar {
  position: absolute;
  left: 0;
  top: 0;
  width: var(--sidebar-width);
  height: 100%;
  background: linear-gradient(
    135deg,
    var(--primary-color) 0%,
    var(--secondary-color) 100%
  );
  color: var(--text-light);
  transform: translateX(
    calc(var(--sidebar-collapsed-width) - var(--sidebar-width))
  );
  transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex;
  flex-direction: column;
  overflow: hidden;

  /* 边缘感应条的颜色暗示 */
  border-right: 4px solid rgba(255, 255, 255, 0.4);
}

.logo {
  height: 80px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  font-size: 20px;
  font-weight: bold;
  letter-spacing: 2px;
  white-space: nowrap;

  .title {
    margin-left: 10px;
  }
}

.nav-menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px 0;

  .nav-item {
    display: flex;
    align-items: center;
    padding: 15px 25px;
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    font-size: 16px;
    transition: all 0.3s ease;
    white-space: nowrap;

    .el-icon {
      margin-right: 15px;
      font-size: 20px;
    }

    &:hover,
    &.active {
      background: rgba(255, 255, 255, 0.2);
      color: #ffffff;
      border-left: 4px solid #ffffff;
    }
  }
}
</style>
