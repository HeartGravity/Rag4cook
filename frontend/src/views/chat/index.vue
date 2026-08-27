<!-- src/views/chat/index.vue -->
<template>
  <div class="page-container">
    <div class="glass-panel chat-wrapper">
      <div class="chat-header">
        <h2>智能厨师对话</h2>
        <p>基于图 RAG 的 AI 烹饪助手</p>
      </div>

      <!-- 聊天记录区域 -->
      <div class="chat-history" ref="chatHistoryRef">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="[
            'message-container',
            msg.role === 'user' ? 'user-container' : 'ai-container',
          ]"
        >
          <div
            :class="[
              'message',
              msg.role === 'user' ? 'user-message' : 'ai-message',
            ]"
          >
            <div
              v-if="msg.role === 'ai'"
              class="markdown-body"
              v-html="renderMarkdown(msg.content)"
            ></div>
            <div v-else>{{ msg.content }}</div>
            <div v-if="msg.strategy" class="strategy-tag">
              策略: {{ msg.strategy }}
            </div>
          </div>
        </div>
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
import MarkdownIt from "markdown-it";
import { useSettingsStore } from "@/stores/settings";

const md = new MarkdownIt({ breaks: true });
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

const renderMarkdown = (text: string) => md.render(text);

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

  // 占位 AI 回复
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
      buffer = lines.pop() || ""; // 保留未完整的块

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
/* 继承你原有的样式 */
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
}
.chat-history {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.message-container {
  display: flex;
  width: 100%;
}
.user-container {
  justify-content: flex-end;
}
.ai-container {
  justify-content: flex-start;
}
.message {
  padding: 12px 18px;
  border-radius: 12px;
  max-width: 70%;
  line-height: 1.5;
}
.user-message {
  background: linear-gradient(
    135deg,
    var(--primary-color),
    var(--secondary-color)
  );
  color: white;
  border-bottom-right-radius: 2px;
}
.ai-message {
  background: #fff;
  color: #333;
  border: 1px solid #eee;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
  border-bottom-left-radius: 2px;
}
.strategy-tag {
  font-size: 12px;
  color: #999;
  margin-top: 8px;
  font-style: italic;
}
.chat-input {
  margin-top: 15px;
}
</style>
