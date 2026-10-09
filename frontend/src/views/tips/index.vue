<!-- src/views/tips/index.vue -->
<template>
  <div class="page-container">
    <div class="tips-layout">
      <!-- 顶部 Header 仪表盘 -->
      <div class="header-dashboard glass-panel">
        <div class="title-meta">
          <div class="badge-icon">
            <el-icon><Opportunity /></el-icon>
          </div>
          <div>
            <h2>厨房秘籍与技巧</h2>
            <p>基于知识图谱的烹饪避坑指南、刀工火候与食材处理技巧</p>
          </div>
        </div>

        <!-- 关键词搜索框 -->
        <div class="search-input-box">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索技巧、厨具或避坑指南..."
            clearable
            @keyup.enter="handleSearch"
            @clear="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
            <template #append>
              <el-button type="primary" @click="handleSearch">搜索</el-button>
            </template>
          </el-input>
        </div>
      </div>

      <!-- 横向滚动分类胶囊栏 -->
      <div class="category-pills-bar">
        <div
          :class="['pill-item', activeCategory === '全部' ? 'active' : '']"
          @click="selectCategory('全部')"
        >
          全部妙招
        </div>
        <div
          v-for="cat in categories"
          :key="cat.name"
          :class="['pill-item', activeCategory === cat.name ? 'active' : '']"
          @click="selectCategory(cat.name)"
        >
          {{ cat.name }}
          <span class="count-badge">{{ cat.count }}</span>
        </div>
      </div>

      <!-- 卡片网格展示区 -->
      <div v-loading="loading" class="cards-grid-container">
        <el-empty
          v-if="!loading && items.length === 0"
          description="未查找到符合条件的厨房技巧"
        />

        <div v-else class="tips-grid">
          <div
            v-for="item in items"
            :key="item.id"
            class="tip-grid-card"
            @click="openTipDetail(item.id)"
          >
            <!-- 卡片顶栏 -->
            <div class="card-top">
              <span class="tip-cat-chip">{{ item.category }}</span>
              <span v-if="item.time_estimate" class="tip-time"
                >⏱ {{ item.time_estimate }}</span
              >
            </div>

            <!-- 卡片标题 -->
            <h3 class="tip-title">{{ item.title }}</h3>

            <!-- 描述摘要 -->
            <p class="tip-desc">
              {{
                item.description ||
                item.methods ||
                "点击查看该秘籍的详细实践要点与操作步骤..."
              }}
            </p>

            <!-- 核心标签/特性标识 -->
            <div class="feature-indicators">
              <span v-if="item.safety_warnings" class="feature-tag warning">
                <el-icon><Warning /></el-icon> 避坑预警
              </span>
              <span v-if="item.tools" class="feature-tag tool">
                <el-icon><Tools /></el-icon> 工具推荐
              </span>
              <span v-if="item.tags?.length" class="feature-tag custom">
                #{{ item.tags[0] }}
              </span>
            </div>

            <!-- 底部操作区 -->
            <div class="card-footer">
              <span class="more-link">查看秘籍详情 →</span>
            </div>
          </div>
        </div>

        <!-- 分页组件 -->
        <div v-if="total > pageSize" class="pagination-box">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[12, 24, 36]"
            layout="total, sizes, prev, pager, next"
            :total="total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </div>

    <!-- 技巧详情弹窗 -->
    <TipDetailModal v-model="detailModalVisible" :tip-id="selectedTipId" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { Opportunity, Search, Warning, Tools } from "@element-plus/icons-vue";
import { getTipCategories, getTipItems } from "@/api/tip";
import TipDetailModal from "@/components/TipDetailModal.vue";

const categories = ref<{ name: string; count: number }[]>([]);
const activeCategory = ref("全部");
const searchKeyword = ref("");

const items = ref<any[]>([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(12);
const loading = ref(false);

const detailModalVisible = ref(false);
const selectedTipId = ref<string | null>(null);

const loadCategories = async () => {
  try {
    const res = await getTipCategories();
    categories.value = res.data.categories || [];
  } catch (err) {
    console.error("加载分类失败", err);
  }
};

const fetchTips = async () => {
  loading.value = true;
  try {
    const res = await getTipItems({
      category: activeCategory.value,
      keyword: searchKeyword.value,
      page: currentPage.value,
      page_size: pageSize.value,
    });
    items.value = res.data.items || [];
    total.value = res.data.total || 0;
  } catch (err) {
    console.error("加载技巧列表失败", err);
  } finally {
    loading.value = false;
  }
};

const selectCategory = (catName: string) => {
  activeCategory.value = catName;
  currentPage.value = 1;
  fetchTips();
};

const handleSearch = () => {
  currentPage.value = 1;
  fetchTips();
};

const handleSizeChange = (val: number) => {
  pageSize.value = val;
  currentPage.value = 1;
  fetchTips();
};

const handleCurrentChange = (val: number) => {
  currentPage.value = val;
  fetchTips();
};

const openTipDetail = (tipId: string) => {
  selectedTipId.value = tipId;
  detailModalVisible.value = true;
};

onMounted(() => {
  loadCategories();
  fetchTips();
});
</script>

<style scoped lang="scss">
.page-container {
  height: 100%;
  overflow-y: auto;
}

.tips-layout {
  padding-bottom: 30px;
}

.header-dashboard {
  padding: 24px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 16px;

  .title-meta {
    display: flex;
    align-items: center;
    gap: 16px;

    .badge-icon {
      width: 52px;
      height: 52px;
      border-radius: 14px;
      background: linear-gradient(135deg, #f7a072, #f62780);
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 26px;
      box-shadow: 0 6px 18px rgba(246, 39, 128, 0.25);
    }

    h2 {
      margin: 0 0 4px;
      font-size: 22px;
      color: #333;
    }

    p {
      margin: 0;
      color: #777;
      font-size: 13px;
    }
  }

  .search-input-box {
    width: 320px;
  }
}

.category-pills-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 22px;
  overflow-x: auto;
  padding-bottom: 6px;

  &::-webkit-scrollbar {
    height: 4px;
  }

  .pill-item {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 18px;
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(0, 0, 0, 0.06);
    border-radius: 20px;
    cursor: pointer;
    font-size: 14px;
    color: #666;
    white-space: nowrap;
    transition: all 0.25s ease;

    .count-badge {
      background: rgba(0, 0, 0, 0.05);
      font-size: 11px;
      padding: 1px 6px;
      border-radius: 10px;
      color: #888;
    }

    &:hover {
      background: #fff;
      transform: translateY(-1px);
    }

    &.active {
      background: linear-gradient(135deg, #f7a072, #e65100);
      color: #fff;
      border-color: transparent;
      box-shadow: 0 4px 12px rgba(230, 81, 0, 0.25);

      .count-badge {
        background: rgba(255, 255, 255, 0.25);
        color: #fff;
      }
    }
  }
}

.cards-grid-container {
  min-height: 240px;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.tip-grid-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 20px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);

  &:hover {
    transform: translateY(-5px);
    background: #ffffff;
    box-shadow: 0 12px 24px rgba(247, 160, 114, 0.15);
    border-color: rgba(247, 160, 114, 0.4);

    .more-link {
      color: #e65100;
      transform: translateX(4px);
    }
  }

  .card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;

    .tip-cat-chip {
      font-size: 12px;
      font-weight: 600;
      color: #e65100;
      background: #fff3e0;
      padding: 3px 10px;
      border-radius: 12px;
    }

    .tip-time {
      font-size: 12px;
      color: #999;
    }
  }

  .tip-title {
    margin: 0 0 10px;
    font-size: 17px;
    color: #2c3e50;
    font-weight: 600;
    line-height: 1.4;
  }

  .tip-desc {
    font-size: 13px;
    color: #666;
    line-height: 1.6;
    margin: 0 0 14px;
    flex: 1;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .feature-indicators {
    display: flex;
    gap: 6px;
    margin-bottom: 14px;
    flex-wrap: wrap;

    .feature-tag {
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      gap: 3px;

      &.warning {
        background: #fbe9e7;
        color: #d84315;
      }
      &.tool {
        background: #ede7f6;
        color: #5e35b1;
      }
      &.custom {
        background: #f5f5f5;
        color: #888;
      }
    }
  }

  .card-footer {
    border-top: 1px solid rgba(0, 0, 0, 0.04);
    padding-top: 10px;
    display: flex;
    justify-content: flex-end;

    .more-link {
      font-size: 12px;
      font-weight: 500;
      color: var(--primary-color);
      transition: all 0.2s ease;
    }
  }
}

.pagination-box {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
</style>
