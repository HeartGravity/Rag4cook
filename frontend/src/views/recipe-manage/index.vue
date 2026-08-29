<!-- src/views/recipe-manage/index.vue -->
<template>
  <div class="page-container">
    <div class="glass-panel content-wrapper">
      <div class="manage-header">
        <div>
          <h2>菜谱管理</h2>
          <p>上传 Markdown 菜谱，经由 AI 解析后入库 RAG 图谱</p>
        </div>
        <el-button type="primary" round @click="dialogVisible = true"
          >上传新菜谱</el-button
        >
      </div>

      <!-- 简单的静态表格占位，实际可接后端获取全部菜谱接口 -->
      <el-table
        :data="tableData"
        style="width: 100%; margin-top: 20px"
        empty-text="暂无数据"
      >
        <el-table-column prop="name" label="菜谱名称" width="180" />
        <el-table-column prop="category" label="分类" width="120" />
        <el-table-column prop="difficulty" label="难度" />
        <el-table-column label="操作" width="150">
          <template #default>
            <el-button link type="primary" size="small">编辑</el-button>
            <el-button link type="danger" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 上传菜谱弹窗 -->
      <el-dialog v-model="dialogVisible" title="上传菜谱" width="500px">
        <el-form label-width="100px">
          <el-form-item label="所属分类">
            <el-input
              v-model="uploadForm.category"
              placeholder="例如: 荤菜 / 素菜"
            />
          </el-form-item>
          <el-form-item label="Markdown文件">
            <input type="file" accept=".md" @change="onMdChange" />
          </el-form-item>
          <el-form-item label="成品图片(可选)">
            <input type="file" accept="image/*" @change="onImageChange" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitUpload" :loading="uploading"
              >上传并解析</el-button
            >
          </span>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { uploadRecipe } from "@/api/recipe";

const tableData = ref([]); // 实际项目中此处应调用获取列表接口
const dialogVisible = ref(false);
const uploading = ref(false);

const uploadForm = ref({
  category: "",
  mdFile: null as File | null,
  imageFile: null as File | null,
});

const onMdChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (target.files && target.files.length)
    uploadForm.value.mdFile = target.files[0];
};

const onImageChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (target.files && target.files.length)
    uploadForm.value.imageFile = target.files[0];
};

const submitUpload = async () => {
  if (!uploadForm.value.mdFile) {
    ElMessage.warning("请选择 Markdown 菜谱文件");
    return;
  }

  const formData = new FormData();
  formData.append("file", uploadForm.value.mdFile);
  formData.append("category", uploadForm.value.category);
  if (uploadForm.value.imageFile) {
    formData.append("image", uploadForm.value.imageFile);
  }

  uploading.value = true;
  try {
    const res = await uploadRecipe(formData);
    ElMessage.success(res.data.message || "上传并解析成功");
    dialogVisible.value = false;
    // TODO: 重新获取 tableData
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || "上传失败");
  } finally {
    uploading.value = false;
  }
};
</script>

<style scoped lang="scss">
/* 基础样式复用[cite: 7] */
.page-container {
  height: 100%;
  overflow-y: auto;
}
.content-wrapper {
  padding: 30px;
  min-height: 100%;
  box-sizing: border-box;
}
.manage-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
h2 {
  color: var(--primary-color);
  margin-top: 0;
  margin-bottom: 5px;
}
p {
  color: #666;
  margin: 0;
}
</style>
