<!-- src/views/home/index.vue -->
<template>
  <div class="home-container">
    <!-- 头部横幅 -->
    <div class="header-section glass-panel">
      <div class="intro">
        <h1>今天想做点什么</h1>
        <p>基于知识图谱和向量数据库的高级烹饪灵感平台</p>
      </div>
      <div class="action">
        <el-button
          type="warning"
          size="large"
          class="chat-btn"
          @click="goToChat"
          round
        >
          <el-icon class="el-icon--left"><ChatLineRound /></el-icon>
          问问你的AI小厨
        </el-button>
      </div>
    </div>

    <!-- 推荐区域 -->
    <div class="recommend-section">
      <div class="section-header">
        <h2 class="section-title">今日推荐</h2>
        <span class="section-subtitle">基于图谱的智能菜谱推荐</span>
      </div>

      <!-- 菜谱网格 -->
      <div class="recipe-grid" v-loading="loading">
        <RecipeCard
          v-for="recipe in recommendedRecipes"
          :key="recipe.id"
          :recipe="recipe"
          @click="openDetail(recipe.id)"
        />
      </div>

      <!-- 换一批推荐按钮（取代独立的推荐页） -->
      <div class="refresh-box">
        <el-button
          type="warning"
          size="large"
          class="refresh-btn"
          :loading="loading"
          round
          @click="fetchRecommendations"
        >
          <el-icon class="el-icon--left"><Refresh /></el-icon>
          换一批推荐
        </el-button>
      </div>
    </div>

    <!-- 菜谱详情弹窗 -->
    <RecipeDetailModal
      v-model="detailModalVisible"
      :recipe-id="selectedRecipeId"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"; // 新增引入
import { useRouter } from "vue-router";
import { ChatLineRound } from "@element-plus/icons-vue";
import RecipeCard from "@/components/RecipeCard.vue";
import RecipeDetailModal from "@/components/RecipeDetailModal.vue";
import { getRecommendRecipes } from "@/api/recipe"; // 引入获取推荐菜谱的API

const router = useRouter();
const recommendedRecipes = ref<any[]>([]); // 替换原来的 mockRecipes
const loading = ref(false);

const detailModalVisible = ref(false);
const selectedRecipeId = ref<string | null>(null);

const fetchRecommendations = async () => {
  loading.value = true;
  try {
    const res = await getRecommendRecipes(4);
    recommendedRecipes.value = res.data;
  } catch (error) {
    console.error("获取推荐菜谱失败:", error);
  } finally {
    loading.value = false;
  }
};

const openDetail = (recipeId: string) => {
  selectedRecipeId.value = recipeId;
  detailModalVisible.value = true;
};

const goToChat = () => router.push("/chat");

onMounted(() => {
  fetchRecommendations();
});
</script>

<style scoped lang="scss">
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  animation: slideUp 0.6s ease;
}
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.glass-panel {
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 16px;
}
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 40px;
  margin-bottom: 40px;
  box-shadow: 0 8px 32px rgba(255, 106, 0, 0.1);
  .intro {
    flex: 1;
    h1 {
      color: var(--primary-color);
      margin-top: 0;
      font-size: 32px;
    }
    p {
      color: #555;
      font-size: 16px;
      line-height: 1.6;
    }
  }
  .chat-btn {
    font-size: 18px;
    padding: 24px 40px;
    background: linear-gradient(
      45deg,
      var(--primary-color),
      var(--secondary-color)
    );
    border: none;
    transition: transform 0.2s;
    &:hover {
      transform: scale(1.05);
      box-shadow: 0 8px 20px rgba(238, 9, 121, 0.3);
    }
  }
}

.recommend-section {
  .section-header {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 20px;

    .section-title {
      color: #333;
      margin: 0;
      font-size: 24px;
    }

    .section-subtitle {
      color: #888;
      font-size: 14px;
    }
  }

  .recipe-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    min-height: 200px;
  }

  .refresh-box {
    margin-top: 40px;
    display: flex;
    justify-content: center;

    .refresh-btn {
      padding: 16px 40px;
      font-size: 16px;
      background: linear-gradient(45deg, #f7a072, #f59e0b);
      border: none;
      box-shadow: 0 6px 16px rgba(245, 158, 11, 0.25);
      transition: all 0.3s;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(245, 158, 11, 0.35);
      }
    }
  }
}
</style>
