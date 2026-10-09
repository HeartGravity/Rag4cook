<!-- src/components/RecipeDetailModal.vue -->
<template>
  <el-dialog
    v-model="visible"
    :show-close="true"
    width="720px"
    class="recipe-detail-dialog"
    destroy-on-close
    append-to-body
    @close="handleClose"
  >
    <div v-loading="loading" class="detail-container">
      <template v-if="recipe">
        <!-- 头部区域 -->
        <div class="modal-header">
          <div class="title-row">
            <h2>{{ recipe.name }}</h2>
            <div class="header-actions">
              <el-button
                circle
                :type="isFav ? 'danger' : 'default'"
                @click="toggleFavorite"
              >
                <el-icon><StarFilled v-if="isFav" /><Star v-else /></el-icon>
              </el-button>
            </div>
          </div>

          <div class="meta-row">
            <el-tag type="warning" effect="dark" round>
              难度: {{ recipe.difficulty }} 星
            </el-tag>
            <el-tag v-if="recipe.category" type="info" round>{{
              recipe.category
            }}</el-tag>
            <el-tag v-if="recipe.cuisine_type" type="success" round>{{
              recipe.cuisine_type
            }}</el-tag>
            <span v-if="recipe.prep_time" class="time-item"
              >⏱ 准备: {{ recipe.prep_time }}</span
            >
            <span v-if="recipe.cook_time" class="time-item"
              >🔥 烹饪: {{ recipe.cook_time }}</span
            >
            <span v-if="recipe.servings" class="time-item"
              >🍽 {{ recipe.servings }}</span
            >
          </div>

          <div v-if="recipe.tags && recipe.tags.length" class="tags-row">
            <el-tag
              v-for="tag in recipe.tags"
              :key="tag"
              size="small"
              class="custom-tag"
            >
              # {{ tag }}
            </el-tag>
          </div>
        </div>

        <!-- 描述/简介 -->
        <div v-if="recipe.description" class="section-box description-box">
          <p>{{ recipe.description }}</p>
        </div>

        <!-- 食材准备 -->
        <div
          v-if="recipe.ingredients && recipe.ingredients.length"
          class="section-box"
        >
          <h3 class="section-title">
            <el-icon><Dish /></el-icon> 必备食材
          </h3>
          <div class="ingredients-grid">
            <div
              v-for="(ing, idx) in recipe.ingredients"
              :key="idx"
              class="ingredient-item"
            >
              <span class="ing-name">{{ ing.name }}</span>
              <span class="ing-amount">
                {{ ing.amount || "" }}{{ ing.unit || "" }}
              </span>
            </div>
          </div>
        </div>

        <!-- 烹饪步骤 -->
        <div v-if="recipe.steps && recipe.steps.length" class="section-box">
          <h3 class="section-title">
            <el-icon><List /></el-icon> 烹饪步骤
          </h3>
          <div class="steps-timeline">
            <div
              v-for="(step, idx) in recipe.steps"
              :key="idx"
              class="step-card"
            >
              <div class="step-num">{{ idx + 1 }}</div>
              <div class="step-body">
                <div class="step-title">{{ step.name }}</div>
                <div v-if="step.description" class="step-desc">
                  {{ step.description }}
                </div>
                <div class="step-extra">
                  <span v-if="step.methods">烹饪技法: {{ step.methods }}</span>
                  <span v-if="step.tools">使用厨具: {{ step.tools }}</span>
                  <span v-if="step.timeEstimate"
                    >预估耗时: {{ step.timeEstimate }}</span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 自定义长文本 / Markdown 内容兼容 -->
        <div
          v-if="!recipe.steps?.length && (recipe.content || recipe.description)"
          class="section-box markdown-box"
          v-html="renderMarkdown(recipe.content || recipe.description)"
        ></div>

        <div
          v-if="
            !recipe.steps?.length &&
            !recipe.ingredients?.length &&
            !recipe.description &&
            !recipe.content
          "
          class="section-box"
        >
          <el-empty description="图谱中暂无该菜谱的关联食材与制作步骤" />
        </div>
      </template>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { Star, StarFilled, Dish, List } from "@element-plus/icons-vue";
import MarkdownIt from "markdown-it";
import { getRecipeDetail } from "@/api/recipe";
import { useFavoriteStore } from "@/stores/favorite";

const md = new MarkdownIt({ breaks: true });
const renderMarkdown = (text: string) => md.render(text || "");

const props = defineProps<{
  modelValue: boolean;
  recipeId: string | null;
}>();

const emit = defineEmits(["update:modelValue"]);

const favoriteStore = useFavoriteStore();
const visible = ref(props.modelValue);
const loading = ref(false);
const recipe = ref<any>(null);

watch(
  () => props.modelValue,
  (val) => {
    visible.value = val;
    if (val && props.recipeId) {
      loadDetail(props.recipeId);
    }
  },
);

const isFav = computed(() => {
  return recipe.value ? favoriteStore.isFavorite(recipe.value.id) : false;
});

const toggleFavorite = () => {
  if (!recipe.value) return;
  favoriteStore.toggleFavorite({
    id: recipe.value.id,
    name: recipe.value.name,
    type: "recipe",
    tags: recipe.value.tags,
  });
};

const loadDetail = async (id: string) => {
  loading.value = true;
  try {
    const res = await getRecipeDetail(id);
    recipe.value = res.data;
  } catch (err) {
    console.error("加载菜谱详情失败", err);
  } finally {
    loading.value = false;
  }
};

const handleClose = () => {
  emit("update:modelValue", false);
  recipe.value = null;
};
</script>

<style lang="scss">
/* 全局弹窗遮罩及毛玻璃高斯模糊滤镜 */
.el-overlay {
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  background-color: rgba(22, 23, 29, 0.45) !important;
}

.recipe-detail-dialog {
  border-radius: 20px !important;
  background: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(16px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15) !important;
  overflow: hidden;

  .el-dialog__header {
    margin-right: 0;
    padding-bottom: 0;
  }

  .el-dialog__body {
    padding: 10px 30px 30px 30px;
    max-height: 75vh;
    overflow-y: auto;
  }
}
</style>

<style scoped lang="scss">
.detail-container {
  min-height: 200px;
}

.modal-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  padding-bottom: 16px;
  margin-bottom: 18px;

  .title-row {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2 {
      margin: 0;
      color: #333;
      font-size: 26px;
    }
  }

  .meta-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 12px;
    flex-wrap: wrap;

    .time-item {
      font-size: 13px;
      color: #777;
    }
  }

  .tags-row {
    display: flex;
    gap: 8px;
    margin-top: 10px;
    flex-wrap: wrap;

    .custom-tag {
      background: rgba(247, 160, 114, 0.1);
      border: 1px solid rgba(247, 160, 114, 0.3);
      color: var(--primary-color);
    }
  }
}

.section-box {
  margin-bottom: 22px;

  .section-title {
    margin: 0 0 12px 0;
    font-size: 17px;
    color: #444;
    display: flex;
    align-items: center;
    gap: 6px;
  }
}

.description-box {
  background: rgba(247, 160, 114, 0.06);
  padding: 14px 18px;
  border-radius: 12px;
  p {
    margin: 0;
    color: #555;
    line-height: 1.6;
    font-size: 14px;
  }
}

.ingredients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 10px;

  .ingredient-item {
    display: flex;
    justify-content: space-between;
    background: #fbfbf7;
    border: 1px solid #eee;
    padding: 10px 14px;
    border-radius: 8px;

    .ing-name {
      font-weight: 500;
      color: #333;
    }

    .ing-amount {
      color: var(--primary-color);
      font-weight: 600;
      font-size: 13px;
    }
  }
}

.steps-timeline {
  display: flex;
  flex-direction: column;
  gap: 14px;

  .step-card {
    display: flex;
    gap: 14px;
    background: #fff;
    border: 1px solid rgba(0, 0, 0, 0.05);
    border-radius: 12px;
    padding: 14px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);

    .step-num {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: linear-gradient(
        135deg,
        var(--primary-color),
        var(--secondary-color)
      );
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-size: 14px;
      flex-shrink: 0;
    }

    .step-body {
      flex: 1;

      .step-title {
        font-weight: 600;
        font-size: 15px;
        color: #333;
        margin-bottom: 6px;
      }

      .step-desc {
        color: #666;
        font-size: 14px;
        line-height: 1.5;
      }

      .step-extra {
        margin-top: 8px;
        display: flex;
        gap: 15px;
        font-size: 12px;
        color: #999;
      }
    }
  }
}

.markdown-box {
  line-height: 1.6;
  color: #444;
}
</style>
