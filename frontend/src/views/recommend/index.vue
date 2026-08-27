<!-- src/views/recommend/index.vue -->
<template>
  <div class="page-container">
    <div class="glass-panel content-wrapper">
      <h2>今日推荐</h2>
      <p>基于图谱的智能菜谱推荐</p>

      <div v-if="loading" class="loading-box" v-loading="loading">
        正在获取推荐...
      </div>

      <div v-else class="recipe-grid">
        <el-card
          v-for="recipe in recipes"
          :key="recipe.id"
          class="recipe-card"
          shadow="hover"
        >
          <img
            v-if="recipe.image_url"
            :src="recipe.image_url"
            class="recipe-image-real"
          />
          <div v-else class="recipe-image-placeholder">
            <el-icon :size="40" color="#ff9a9e"><Dish /></el-icon>
          </div>
          <div class="recipe-info">
            <h3>{{ recipe.name }}</h3>
            <div class="tags">
              <el-tag size="small" type="danger" effect="plain"
                >难度: {{ recipe.difficulty }}星</el-tag
              >
              <el-tag
                v-for="tag in recipe.tags.slice(0, 2)"
                :key="tag"
                size="small"
                type="info"
                >{{ tag }}</el-tag
              >
            </div>
          </div>
        </el-card>
      </div>

      <div class="random-box">
        <el-button
          type="warning"
          size="large"
          @click="fetchRecommendations"
          :loading="loading"
          round
          >换一批推荐</el-button
        >
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { Dish } from "@element-plus/icons-vue";
import { getRecommendRecipes } from "@/api/recipe";

const recipes = ref<any[]>([]);
const loading = ref(false);

const fetchRecommendations = async () => {
  loading.value = true;
  try {
    const res = await getRecommendRecipes(4);
    recipes.value = res.data;
  } catch (error) {
    console.error("获取推荐失败", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchRecommendations();
});
</script>

<style scoped lang="scss">
/* 借用 Home 页面已有的 grid 样式[cite: 7] */
.page-container {
  height: 100%;
  overflow-y: auto;
}
.content-wrapper {
  padding: 30px;
  min-height: 100%;
  box-sizing: border-box;
}
.recipe-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
.recipe-card {
  border: none;
  cursor: pointer;
  transition: transform 0.3s;
  &:hover {
    transform: translateY(-5px);
  }
}
.recipe-image-placeholder {
  height: 160px;
  background: rgba(255, 106, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
}
.recipe-image-real {
  width: 100%;
  height: 160px;
  object-fit: cover;
}
.recipe-info h3 {
  margin: 15px 0 10px;
}
.tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.random-box {
  margin-top: 50px;
  display: flex;
  justify-content: center;
}
</style>
