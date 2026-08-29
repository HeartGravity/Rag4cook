<!-- src/views/chat/index.vue -->
<template>
  <div class="page-container">
    <div class="glass-panel chat-wrapper">
      <div class="chat-header">
        <h2>智能厨师对话</h2>
        <p>基于图 RAG 的 AI 烹饪助手</p>
      </div>

      <!-- 聊天记录区域 (使用通用组件替换) -->
      <div class="chat-history" ref="chatHistoryRef">
        <ChatMessage v-for="(msg, index) in messages" :key="index" :msg="msg" />
      </div>

      <!-- 输入区域 -->
      <div class="chat-input">
        <el-input
          v-model="inputMsg"
          placeholder="问点什么吧，比如：红烧肉怎么做？"
          size="large"
          @keyup.enter="sendMessage"
          :disabled="isGenerating"
        >
          <template #append>
            <el-button
              type="primary"
              @click="sendMessage"
              :loading="isGenerating"
              >发送</el-button
            >
          </template>
        </el-input>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from "vue";
import { useSettingsStore } from "@/stores/settings";
import ChatMessage from "@/components/ChatMessage.vue"; // 引入通用气泡组件

const settings = useSettingsStore();

interface Message {
  role: "user" | "ai";
  content: string;
  strategy?: string;
}

const inputMsg = ref("");
const messages = ref<Message[]>([
  { role: "ai", content: "你好！我是你的智能烹饪助手。有什么我可以帮你的吗？" },
]);
const isGenerating = ref(false);
const chatHistoryRef = ref<HTMLElement | null>(null);

const scrollToBottom = async () => {
  await nextTick();
  if (chatHistoryRef.value) {
    chatHistoryRef.value.scrollTop = chatHistoryRef.value.scrollHeight;
  }
};

const sendMessage = async () => {
  if (!inputMsg.value.trim() || isGenerating.value) return;

  const query = inputMsg.value;
  messages.value.push({ role: "user", content: query });
  inputMsg.value = "";
  isGenerating.value = true;

  messages.value.push({ role: "ai", content: "" });
  const currentAiIndex = messages.value.length - 1;
  scrollToBottom();

  try {
    const response = await fetch(`${settings.apiUrl}/api/chat/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: query,
        stream: true,
        explain_routing: true,
      }),
    });

    if (!response.body) throw new Error("No response body");

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const dataStr = line.slice(6).trim();
          if (dataStr === "[DONE]") break;
          try {
            const data = JSON.parse(dataStr);
            messages.value[currentAiIndex].content += data.content;
            scrollToBottom();
          } catch (e) {
            console.error("Parse error", dataStr);
          }
        }
      }
    }
  } catch (error) {
    messages.value[currentAiIndex].content =
      "网络请求失败，请检查后端服务是否启动。";
  } finally {
    isGenerating.value = false;
  }
};
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
  display: flex;
  flex-direction: column;
}
.chat-input {
  margin-top: 15px;
}
</style>
