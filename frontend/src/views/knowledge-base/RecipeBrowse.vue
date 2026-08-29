<!-- src/views/knowledge-base/RecipeBrowse.vue -->
<template>
  <div class="page-container">
    <div class="glass-panel content-wrapper">
      <h2>厨房知识库</h2>
      <p>探索 Neo4j 图数据库中的烹饪智慧</p>

      <div class="knowledge-layout">
        <!-- 左侧分类 -->
        <div class="category-sidebar">
          <div
            v-for="cat in categories"
            :key="cat"
            :class="['category-item', activeCategory === cat ? 'active' : '']"
            @click="selectCategory(cat)"
          >
            {{ cat }}
          </div>
        </div>

        <!-- 右侧内容 -->
        <div class="knowledge-content" v-loading="loading">
          <el-empty v-if="items.length === 0" description="该分类下暂无数据" />
          <!-- 替换为通用组件 -->
          <KnowledgeCard v-for="item in items" :key="item.id" :item="item" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getKnowledgeCategories, getKnowledgeItems } from "@/api/recipe";
import KnowledgeCard from "@/components/KnowledgeCard.vue"; // 引入通用卡片组件

const categories = ref<string[]>([]);
const activeCategory = ref("");
const items = ref<any[]>([]);
const loading = ref(false);

const loadCategories = async () => {
  try {
    const res = await getKnowledgeCategories();
    categories.value = res.data.categories || [];
    if (categories.value.length > 0) {
      selectCategory(categories.value[0]);
    }
  } catch (e) {
    console.error("加载分类失败", e);
  }
};

const selectCategory = async (cat: string) => {
  activeCategory.value = cat;
  loading.value = true;
  try {
    const res = await getKnowledgeItems(cat);
    items.value = res.data || [];
  } catch (e) {
    console.error("加载知识项失败", e);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadCategories();
});
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
.knowledge-layout {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}
.category-sidebar {
  width: 200px;
  border-right: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.category-item {
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s;
  color: #555;
}
.category-item:hover {
  background: rgba(0, 0, 0, 0.02);
}
.category-item.active {
  background: var(--primary-color);
  color: white;
}
.knowledge-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
