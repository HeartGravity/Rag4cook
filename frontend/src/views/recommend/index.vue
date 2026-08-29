<!-- src/views/recommend/index.vue -->
<template>
  <div class="page-container">
    <div class="glass-panel content-wrapper">
      <h2>今日推荐</h2>
      <p>基于图谱的智能菜谱推荐</p>

      <div v-if="loading" class="loading-box" v-loading="loading"></div>

      <div v-else class="recipe-grid">
        <!-- 替换为通用组件 -->
        <RecipeCard
          v-for="recipe in recipes"
          :key="recipe.id"
          :recipe="recipe"
        />
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
import { getRecommendRecipes } from "@/api/recipe";
import RecipeCard from "@/components/RecipeCard.vue"; // 引入通用卡片组件

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
.page-container {
  height: 100%;
  overflow-y: auto;
}
.content-wrapper {
  padding: 30px;
  min-height: 100%;
  box-sizing: border-box;
}
.loading-box {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.recipe-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
.random-box {
  margin-top: 50px;
  display: flex;
  justify-content: center;
}
</style>
