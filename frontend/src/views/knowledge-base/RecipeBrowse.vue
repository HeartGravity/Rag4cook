<!-- src/views/knowledge-base/RecipeBrowse.vue -->
<template>
  <div class="page-container">
    <div class="glass-panel content-wrapper">
      <h2>菜谱知识库</h2>
      <p>探索 Neo4j 图谱中的结构化做菜指南</p>
      <div class="knowledge-layout">
        <!-- 分类侧边栏 -->
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

        <!-- 知识列表 -->
        <div class="knowledge-content" v-loading="loading">
          <el-empty v-if="items.length === 0" description="暂无该分类数据" />

          <template v-else>
            <KnowledgeCard
              v-for="item in items"
              :key="item.id"
              :item="item"
              @click="openDetail(item.id)"
            />

            <!-- 分页条 -->
            <div class="pagination-container">
              <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="total"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- 菜谱详情弹窗 -->
    <RecipeDetailModal
      v-model="detailModalVisible"
      :recipe-id="selectedRecipeId"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getKnowledgeCategories, getKnowledgeItems } from "@/api/recipe";
import KnowledgeCard from "@/components/KnowledgeCard.vue";
import RecipeDetailModal from "@/components/RecipeDetailModal.vue";

const categories = ref<string[]>([]);
const activeCategory = ref("");
const items = ref<any[]>([]);
const loading = ref(false);

// 分页状态
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 详情弹窗控制
const detailModalVisible = ref(false);
const selectedRecipeId = ref<string | null>(null);

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

const fetchItems = async () => {
  loading.value = true;
  try {
    const res = await getKnowledgeItems(
      activeCategory.value,
      currentPage.value,
      pageSize.value,
    );
    items.value = res.data.items || [];
    total.value = res.data.total || 0;
  } catch (e) {
    console.error("加载菜谱列表失败", e);
  } finally {
    loading.value = false;
  }
};

const selectCategory = (cat: string) => {
  activeCategory.value = cat;
  currentPage.value = 1; // 切换分类重置页码
  fetchItems();
};

const handleSizeChange = (val: number) => {
  pageSize.value = val;
  currentPage.value = 1;
  fetchItems();
};

const handleCurrentChange = (val: number) => {
  currentPage.value = val;
  fetchItems();
};

const openDetail = (id: string) => {
  selectedRecipeId.value = id;
  detailModalVisible.value = true;
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
  width: 180px;
  border-right: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-shrink: 0;

  .category-item {
    padding: 10px 16px;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.25s;
    color: #555;
    font-size: 15px;

    &:hover {
      background: rgba(0, 0, 0, 0.03);
    }

    &.active {
      background: var(--primary-color);
      color: white;
      font-weight: 500;
    }
  }
}

.knowledge-content {
  flex: 1;
  display: flex;
  flex-direction: column;

  .pagination-container {
    margin-top: 20px;
    margin-bottom: 10px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
