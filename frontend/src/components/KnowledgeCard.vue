<!-- src/components/KnowledgeCard.vue -->
<template>
  <el-card class="knowledge-card" shadow="hover" @click="$emit('click')">
    <div class="card-header">
      <div class="title-with-meta">
        <h3 class="recipe-title">{{ item.title }}</h3>
        <!-- 难度徽标 -->
        <el-tag
          size="small"
          type="warning"
          effect="light"
          round
          class="diff-tag"
        >
          难度: {{ item.difficulty || 3 }}星
        </el-tag>
        <!-- 食材列表 -->
        <div
          v-if="item.ingredients && item.ingredients.length"
          class="ingredients-list"
        >
          <span class="ing-label">用料:</span>
          <el-tag
            v-for="(ing, idx) in item.ingredients.slice(0, 3)"
            :key="idx"
            size="small"
            type="info"
            effect="plain"
            class="ing-tag"
          >
            {{ ing }}
          </el-tag>
          <span v-if="item.ingredients.length > 3" class="more-text">等</span>
        </div>
      </div>

      <el-button
        link
        :type="isFav ? 'danger' : 'primary'"
        @click.stop="toggleFavorite"
      >
        {{ isFav ? "已收藏" : "收藏" }}
      </el-button>
    </div>
    <p class="summary">{{ item.summary }}</p>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useFavoriteStore } from "@/stores/favorite";

const props = defineProps<{ item: any }>();
defineEmits(["click"]);

const favoriteStore = useFavoriteStore();
const isFav = computed(() => favoriteStore.isFavorite(props.item.id));

const toggleFavorite = () => {
  favoriteStore.toggleFavorite({
    id: props.item.id,
    name: props.item.title,
    type: "knowledge",
  });
};
</script>

<style scoped lang="scss">
.knowledge-card {
  margin-bottom: 15px;
  cursor: pointer;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
  border-radius: 12px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;

    .title-with-meta {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;

      .recipe-title {
        margin: 0;
        font-size: 16px;
        color: #333;
        font-weight: 600;
      }

      .diff-tag {
        font-weight: 500;
      }

      .ingredients-list {
        display: flex;
        align-items: center;
        gap: 6px;

        .ing-label {
          font-size: 13px;
          color: #888;
        }

        .ing-tag {
          background-color: #fafafa;
          border-color: #e8e8e8;
          color: #555;
        }

        .more-text {
          font-size: 12px;
          color: #aaa;
        }
      }
    }
  }

  .summary {
    font-size: 14px;
    color: #666;
    line-height: 1.6;
    margin: 0;
  }
}
</style>
