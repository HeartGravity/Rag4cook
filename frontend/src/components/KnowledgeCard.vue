<!-- src/components/KnowledgeCard.vue -->
<template>
  <el-card class="knowledge-card" shadow="hover">
    <div class="card-header">
      <h3>{{ item.title }}</h3>
      <el-button
        link
        :type="isFav ? 'danger' : 'primary'"
        @click="toggleFavorite"
      >
        {{ isFav ? "取消收藏" : "收藏" }}
      </el-button>
    </div>
    <p class="summary">{{ item.summary }}</p>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useFavoriteStore } from "@/stores/favorite";

const props = defineProps<{ item: any }>();
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
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.card-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}
.summary {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin: 0;
}
</style>
