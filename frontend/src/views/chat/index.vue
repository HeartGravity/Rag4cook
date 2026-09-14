<!-- src/views/chat/index.vue -->
<template>
  <div class="page-container">
    <div class="chat-layout">
      <!-- 左侧：历史会话列表 -->
      <div class="glass-panel history-sidebar">
        <div class="history-header">
          <h3>历史对话</h3>
          <el-button type="primary" link icon="Plus" @click="createNewChat"
            >新对话</el-button
          >
        </div>
        <ul class="session-list">
          <li
            v-for="session in chatSessions"
            :key="session.id"
            :class="[
              'session-item',
              { active: currentSessionId === session.id },
            ]"
            @click="switchSession(session.id)"
          >
            <el-icon><ChatLineSquare /></el-icon>
            <span class="session-title">{{ session.title }}</span>
          </li>
        </ul>
      </div>

      <!-- 右侧：当前对话框 -->
      <div class="glass-panel chat-wrapper">
        <div class="chat-header">
          <h2>智能厨师对话</h2>
          <p>基于图 RAG 的 AI 烹饪助手</p>
        </div>

        <div class="chat-history" ref="chatHistoryRef">
          <ChatMessage
            v-for="(msg, index) in currentMessages"
            :key="index"
            :msg="msg"
          />
        </div>

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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from "vue";
import { useSettingsStore } from "@/stores/settings";
import ChatMessage from "@/components/ChatMessage.vue";
import { ChatLineSquare, Plus } from "@element-plus/icons-vue";

const settings = useSettingsStore();

interface Message {
  role: "user" | "ai";
  content: string;
  strategy?: string;
}

interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
}

// 模拟前端历史会话状态
const chatSessions = ref<ChatSession[]>([
  {
    id: "1",
    title: "红烧肉的做法",
    messages: [
      {
        role: "ai",
        content: "你好！我是你的智能烹饪助手。有什么我可以帮你的吗？",
      },
      { role: "user", content: "红烧肉怎么做？" },
      {
        role: "ai",
        content: "红烧肉需要准备五花肉、冰糖、生抽、老抽...",
        strategy: "检索图数据库",
      },
    ],
  },
  {
    id: "2",
    title: "新对话",
    messages: [
      {
        role: "ai",
        content: "你好！我是你的智能烹饪助手。有什么我可以帮你的吗？",
      },
    ],
  },
]);

const currentSessionId = ref<string>("2");

const currentMessages = computed(() => {
  const session = chatSessions.value.find(
    (s) => s.id === currentSessionId.value,
  );
  return session ? session.messages : [];
});

const inputMsg = ref("");
const isGenerating = ref(false);
const chatHistoryRef = ref<HTMLElement | null>(null);

const scrollToBottom = async () => {
  await nextTick();
  if (chatHistoryRef.value) {
    chatHistoryRef.value.scrollTop = chatHistoryRef.value.scrollHeight;
  }
};

const createNewChat = () => {
  const newId = Date.now().toString();
  chatSessions.value.unshift({
    id: newId,
    title: "新对话",
    messages: [
      {
        role: "ai",
        content: "你好！我是你的智能烹饪助手。有什么我可以帮你的吗？",
      },
    ],
  });
  currentSessionId.value = newId;
};

const switchSession = (id: string) => {
  currentSessionId.value = id;
  scrollToBottom();
};

const sendMessage = async () => {
  if (!inputMsg.value.trim() || isGenerating.value) return;
  const query = inputMsg.value;

  // 更新当前会话的 title (如果是新对话的话)
  const currentSession = chatSessions.value.find(
    (s) => s.id === currentSessionId.value,
  );
  if (currentSession && currentSession.title === "新对话") {
    currentSession.title =
      query.slice(0, 10) + (query.length > 10 ? "..." : "");
  }

  currentSession?.messages.push({ role: "user", content: query });
  inputMsg.value = "";
  isGenerating.value = true;

  currentSession?.messages.push({ role: "ai", content: "" });
  const currentAiIndex = (currentSession?.messages.length || 1) - 1;
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
            if (currentSession) {
              currentSession.messages[currentAiIndex].content += data.content;
            }
            scrollToBottom();
          } catch (e) {
            console.error("Parse error", dataStr);
          }
        }
      }
    }
  } catch (error) {
    if (currentSession) {
      currentSession.messages[currentAiIndex].content =
        "抱歉，生成回复时出现错误，请检查后端服务。";
    }
  } finally {
    isGenerating.value = false;
  }
};
</script>

<style scoped lang="scss">
.page-container {
  height: 100%;
}

.chat-layout {
  display: flex;
  gap: 20px;
  height: 100%;
}

/* 左侧历史会话样式 */
.history-sidebar {
  width: 250px;
  display: flex;
  flex-direction: column;
  padding: 15px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  margin-bottom: 10px;

  h3 {
    margin: 0;
    font-size: 16px;
    color: var(--text-main);
  }
}

.session-list {
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
  flex: 1;
}

.session-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  color: #666;
  margin-bottom: 8px;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  &.active {
    background: var(--primary-color);
    color: white;
  }

  .session-title {
    font-size: 14px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

/* 右侧对话区域样式 */
.chat-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
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
