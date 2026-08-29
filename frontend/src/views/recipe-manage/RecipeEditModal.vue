<!-- src/views/recipe-manage/RecipeEditModal.vue -->
<template>
  <el-dialog
    :model-value="visible"
    @update:model-value="$emit('update:visible', $event)"
    :title="isEdit ? '编辑菜谱' : '上传新菜谱'"
    width="500px"
  >
    <el-form label-width="100px" :model="formData">
      <el-form-item label="菜谱名称">
        <el-input
          v-model="formData.name"
          placeholder="请输入菜谱名称"
          :disabled="!isEdit"
        />
      </el-form-item>
      <el-form-item label="所属分类">
        <el-input v-model="formData.category" placeholder="例如: 荤菜 / 素菜" />
      </el-form-item>
      <el-form-item label="难度(星级)">
        <el-rate v-model="formData.difficulty" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="$emit('update:visible', false)">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="loading"
          >保存修改</el-button
        >
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";

const props = defineProps<{ visible: boolean; initialData?: any }>();
const emit = defineEmits(["update:visible", "save"]);

const loading = ref(false);
const isEdit = ref(false);
const formData = ref({ name: "", category: "", difficulty: 3 });

watch(
  () => props.visible,
  (val) => {
    if (val && props.initialData) {
      isEdit.value = true;
      formData.value = { ...props.initialData };
    } else {
      isEdit.value = false;
      formData.value = { name: "", category: "", difficulty: 3 };
    }
  },
);

const handleSave = async () => {
  loading.value = true;
  // 模拟保存逻辑，触发外部事件
  setTimeout(() => {
    emit("save", formData.value);
    loading.value = false;
    emit("update:visible", false);
  }, 1000);
};
</script>
