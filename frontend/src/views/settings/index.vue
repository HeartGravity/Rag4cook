<!-- src/views/settings/index.vue -->
<template>
  <div class="page-container">
    <div class="glass-panel content-wrapper">
      <h2>系统设置</h2>
      <p>配置本地或云端 RAG 引擎的连接信息</p>

      <el-form label-width="120px" class="settings-form">
        <el-form-item label="后端 API 地址">
          <el-input
            v-model="apiUrl"
            placeholder="例如: http://localhost:8000"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveSettings">保存设置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { useSettingsStore } from "@/stores/settings";

const settingsStore = useSettingsStore();
const apiUrl = ref(settingsStore.apiUrl);

const saveSettings = () => {
  if (!apiUrl.value) {
    ElMessage.warning("API 地址不能为空");
    return;
  }
  settingsStore.setApiUrl(apiUrl.value);
  ElMessage.success("设置保存成功！");
};
</script>

<style scoped lang="scss">
/* 基础样式复用[cite: 7] */
.page-container {
  height: 100%;
}
.content-wrapper {
  padding: 30px;
  height: 100%;
  box-sizing: border-box;
}
h2 {
  color: var(--primary-color);
  margin-top: 0;
  margin-bottom: 10px;
}
p {
  color: #666;
  margin-bottom: 30px;
}
.settings-form {
  max-width: 500px;
  margin-top: 20px;
}
</style>
