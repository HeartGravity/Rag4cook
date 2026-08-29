<!-- src/views/home/index.vue -->
<template>
  <div class="home-container">
    <!-- 头部横幅 -->
    <div class="header-section glass-panel">
      <div class="intro">
        <h1>欢迎使用 AI 厨师</h1>
        <p>基于本地 RAG 图数据库构建的智能烹饪与食谱推荐系统</p>
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
          开始对话
        </el-button>
      </div>
    </div>

    <!-- 热门推荐 -->
    <div class="recommend-section">
      <h2 class="section-title">热门推荐</h2>
      <div class="recipe-grid">
        <!-- 替换为通用组件 -->
        <RecipeCard
          v-for="recipe in mockRecipes"
          :key="recipe.id"
          :recipe="recipe"
          @click="goToRecommend"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { ChatLineRound } from "@element-plus/icons-vue";
import RecipeCard from "@/components/RecipeCard.vue"; // 引入通用卡片组件

const router = useRouter();

// 为首页配置一组 Mock 数据来填充 RecipeCard
const mockRecipes = [
  { id: "1", name: "宫保鸡丁", difficulty: 3, tags: ["川菜", "家常菜"] },
  { id: "2", name: "清蒸鲈鱼", difficulty: 2, tags: ["粤菜", "海鲜"] },
  { id: "3", name: "红烧肉", difficulty: 4, tags: ["下饭", "经典"] },
  { id: "4", name: "麻婆豆腐", difficulty: 2, tags: ["川菜", "素食"] },
];

const goToChat = () => router.push("/chat");
const goToRecommend = () => router.push("/recommend");
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
.section-title {
  color: #333;
  margin-bottom: 20px;
  font-size: 24px;
}
.recipe-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}
</style>
