<template>
  <div class="page-container">
    <div class="glass-panel chat-wrapper">
      <div class="chat-header">
        <h2>智能烹饪问答</h2>
        <p>基于本地知识库的专属 AI 厨师</p>
      </div>

      <!-- 聊天记录展示区占位 -->
      <div class="chat-history">
        <div class="message ai-message">
          你好！我是尝尝咸淡智能助手，今天想吃点什么？或者有什么烹饪上的疑问吗？
        </div>
      </div>

      <!-- 输入区占位 -->
      <div class="chat-input">
        <el-input
          v-model="inputMsg"
          placeholder="问点什么，比如：西红柿炒鸡蛋怎么做？"
          size="large"
        >
          <template #append>
            <el-button type="primary">发送</el-button>
          </template>
        </el-input>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const inputMsg = ref("");
</script>

<style scoped lang="scss">
.page-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  background: rgba(255, 255, 255, 0.75);
}

.chat-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding-bottom: 15px;
  h2 {
    margin: 0;
    color: var(--primary-color);
  }
  p {
    margin: 5px 0 0;
    color: #666;
    font-size: 14px;
  }
}

.chat-history {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
  .message {
    padding: 12px 18px;
    border-radius: 12px;
    max-width: 70%;
    margin-bottom: 15px;
    line-height: 1.5;
  }
  .ai-message {
    background: #fff;
    color: #333;
    border: 1px solid #eee;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
  }
}

.chat-input {
  margin-top: 15px;
}
</style>
