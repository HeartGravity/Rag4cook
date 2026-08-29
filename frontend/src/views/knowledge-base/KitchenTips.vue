<!-- src/views/knowledge-base/KitchenTips.vue -->
<template>
  <div class="page-container">
    <div class="glass-panel content-wrapper">
      <h2>厨房基本功</h2>
      <p>新手下厨必看的生存指南</p>

      <div class="tips-grid">
        <el-card
          v-for="(tip, index) in tips"
          :key="index"
          shadow="hover"
          class="tip-card"
        >
          <div class="tip-icon">
            <el-icon :size="30" color="var(--primary-color)"
              ><Opportunity
            /></el-icon>
          </div>
          <div class="tip-content">
            <h4>{{ tip.title }}</h4>
            <p>{{ tip.desc }}</p>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { Opportunity } from "@element-plus/icons-vue";

// 本地静态展示的数据，或者可以对接后端的基础知识表
const tips = ref([
  {
    title: "切洋葱不流泪",
    desc: "切之前将洋葱放冰箱冷藏15分钟，或在水中切，可有效减少对眼睛的刺激。",
  },
  {
    title: "炒青菜保持翠绿",
    desc: "大火快炒，出锅前再放盐。可以在焯水时加入几滴食用油。",
  },
  {
    title: "炖肉更易烂",
    desc: "炖牛羊肉时可以加几片山楂或一小勺茶叶，能够加速肉质软烂。",
  },
  {
    title: "快速解冻肉类",
    desc: "采用铝盆夹肉法或者加入少量盐的温水中浸泡，千万不要用开水直接烫。",
  },
]);
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
.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
.tip-card {
  display: flex;
  flex-direction: row;
  border-radius: 12px;
}
:deep(.el-card__body) {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 20px;
}
.tip-icon {
  background: rgba(255, 106, 0, 0.1);
  padding: 15px;
  border-radius: 50%;
  display: flex;
}
.tip-content h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 16px;
}
.tip-content p {
  margin: 0;
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}
</style>
