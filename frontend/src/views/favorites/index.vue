<!-- src/views/favorites/index.vue -->
<template>
  <div class="page-container">
    <div class="glass-panel content-wrapper">
      <h2>我的收藏</h2>
      <p>您保存的菜谱和厨房小贴士</p>

      <el-empty
        v-if="favoriteStore.favorites.length === 0"
        description="暂无收藏内容"
      />

      <div v-else class="favorite-list">
        <el-card
          v-for="item in favoriteStore.favorites"
          :key="item.id"
          class="favorite-card"
          shadow="hover"
        >
          <div class="card-header">
            <h3>{{ item.name }}</h3>
            <el-tag
              :type="item.type === 'recipe' ? 'success' : 'info'"
              size="small"
            >
              {{ item.type === "recipe" ? "菜谱" : "知识" }}
            </el-tag>
          </div>
          <el-button
            type="danger"
            text
            @click="favoriteStore.toggleFavorite(item)"
            >取消收藏</el-button
          >
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useFavoriteStore } from "@/stores/favorite";
const favoriteStore = useFavoriteStore();
</script>

<style scoped lang="scss">
.page-container {
  height: 100%;
  overflow-y: auto;
}
.content-wrapper {
  padding: 30px;
  min-height: 100%;
  box-sizing: border-box;
}
.favorite-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
}
.favorite-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card-header {
  display: flex;
  align-items: center;
  gap: 15px;
  h3 {
    margin: 0;
  }
}
</style>
