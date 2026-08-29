<!-- src/components/RecipeCard.vue -->
<template>
  <el-card class="recipe-card" shadow="hover" @click="$emit('click')">
    <div class="image-wrapper">
      <img
        v-if="recipe.image_url"
        :src="recipe.image_url"
        class="recipe-image-real"
      />
      <div v-else class="recipe-image-placeholder">
        <el-icon :size="40" color="#ff9a9e"><Dish /></el-icon>
      </div>
      <!-- 收藏按钮层 -->
      <div class="favorite-btn" @click.stop="toggleFavorite">
        <el-icon :color="isFav ? '#f56c6c' : '#fff'" :size="20">
          <StarFilled v-if="isFav" />
          <Star v-else />
        </el-icon>
      </div>
    </div>
    <div class="recipe-info">
      <h3>{{ recipe.name }}</h3>
      <div class="tags">
        <el-tag size="small" type="danger" effect="plain"
          >难度: {{ recipe.difficulty }}星</el-tag
        >
        <el-tag
          v-for="tag in recipe.tags?.slice(0, 2)"
          :key="tag"
          size="small"
          type="info"
          >{{ tag }}</el-tag
        >
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { Dish, Star, StarFilled } from "@element-plus/icons-vue";
import { useFavoriteStore } from "@/stores/favorite";

const props = defineProps<{ recipe: any }>();
defineEmits(["click"]);

const favoriteStore = useFavoriteStore();
const isFav = computed(() => favoriteStore.isFavorite(props.recipe.id));

const toggleFavorite = () => {
  favoriteStore.toggleFavorite({
    id: props.recipe.id,
    name: props.recipe.name,
    type: "recipe",
    tags: props.recipe.tags,
  });
};
</script>

<style scoped lang="scss">
.recipe-card {
  border: none;
  cursor: pointer;
  transition: transform 0.3s;
  position: relative;
  overflow: visible;
  padding: 0;
}
.recipe-card:hover {
  transform: translateY(-5px);
}
.image-wrapper {
  position: relative;
}
.recipe-image-placeholder {
  height: 160px;
  background: rgba(255, 106, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
}
.recipe-image-real {
  width: 100%;
  height: 160px;
  object-fit: cover;
}
.favorite-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  padding: 5px;
  display: flex;
  transition: background 0.3s;
}
.favorite-btn:hover {
  background: rgba(0, 0, 0, 0.6);
}
.recipe-info {
  padding: 15px;
}
.recipe-info h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #333;
}
.tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
</style>
