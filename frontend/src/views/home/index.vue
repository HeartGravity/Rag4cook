<!-- src/views/home/index.vue -->
<template>
  <div class="home-container">
    <!-- 顶部介绍与快捷入口 -->
    <div class="header-section glass-panel">
      <div class="intro">
        <h1>厨房里的智能帮手 👨‍🍳</h1>
        <p>
          尝尝咸淡 RAG
          助手，基于你的专属烹饪知识库。无论是家常炒菜还是烘焙甜点，问我准没错。
        </p>
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
          开始智能对话
        </el-button>
      </div>
    </div>

    <!-- 推荐菜谱区 -->
    <div class="recommend-section">
      <h2 class="section-title">今日灵感推荐 ✨</h2>
      <div class="recipe-grid">
        <el-card
          v-for="i in 4"
          :key="i"
          class="recipe-card glass-panel"
          shadow="hover"
        >
          <div class="recipe-image">
            <el-icon :size="40" color="#ff9a9e"><Dish /></el-icon>
          </div>
          <div class="recipe-info">
            <h3>示例推荐菜谱 {{ i }}</h3>
            <p>香气四溢，简单易学</p>
            <div class="tags">
              <el-tag size="small" type="danger" effect="plain">热菜</el-tag>
              <el-tag size="small" type="warning" effect="plain">15分钟</el-tag>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { ChatLineRound, Dish } from "@element-plus/icons-vue";

const router = useRouter();

const goToChat = () => {
  router.push("/chat");
};
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

/* 磨砂玻璃质感 */
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

  .recipe-card {
    border: none;
    cursor: pointer;
    transition: transform 0.3s;

    &:hover {
      transform: translateY(-5px);
    }

    .recipe-image {
      height: 120px;
      background: rgba(255, 106, 0, 0.05);
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
      margin-bottom: 15px;
    }

    .recipe-info {
      h3 {
        margin: 0 0 10px 0;
        color: #333;
        font-size: 18px;
      }
      p {
        margin: 0 0 15px 0;
        color: #666;
        font-size: 14px;
      }
      .tags {
        display: flex;
        gap: 8px;
      }
    }
  }
}
</style>
