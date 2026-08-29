<!-- src/components/ChatMessage.vue -->
<template>
  <div
    :class="[
      'message-container',
      msg.role === 'user' ? 'user-container' : 'ai-container',
    ]"
  >
    <div
      :class="['message', msg.role === 'user' ? 'user-message' : 'ai-message']"
    >
      <div
        v-if="msg.role === 'ai'"
        class="markdown-body"
        v-html="renderMarkdown(msg.content)"
      ></div>
      <div v-else>{{ msg.content }}</div>
      <div v-if="msg.strategy" class="strategy-tag">
        <el-icon><Guide /></el-icon> 检索策略: {{ msg.strategy }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import MarkdownIt from "markdown-it";
import { Guide } from "@element-plus/icons-vue";

const md = new MarkdownIt({ breaks: true });
const props = defineProps<{
  msg: { role: "user" | "ai"; content: string; strategy?: string };
}>();

const renderMarkdown = (text: string) => md.render(text);
</script>

<style scoped lang="scss">
.message-container {
  display: flex;
  width: 100%;
  margin-bottom: 15px;
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
  display: flex;
  align-items: center;
  gap: 4px;
}
/* 简单的 Markdown 样式重置 */
.markdown-body :deep(p) {
  margin: 0 0 10px 0;
}
.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  margin-top: 0;
  padding-left: 20px;
}
</style>
