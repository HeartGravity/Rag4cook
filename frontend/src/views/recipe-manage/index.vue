<!-- src/views/recipe-manage/index.vue -->
<template>
  <div class="page-container">
    <div class="glass-panel content-wrapper">
      <div class="manage-header">
        <div>
          <h2>菜谱管理</h2>
          <p>管理图数据库中的菜谱节点</p>
        </div>
        <el-button type="primary" round @click="dialogVisible = true">
          上传新菜谱
        </el-button>
      </div>

      <!-- 数据表格 -->
      <el-table
        :data="tableData"
        style="width: 100%; margin-top: 20px"
        empty-text="暂无菜谱数据"
        v-loading="loading"
      >
        <el-table-column prop="name" label="菜谱名称" width="180" />
        <el-table-column prop="category" label="分类" width="120" />
        <el-table-column prop="difficulty" label="难度星级">
          <template #default="scope">
            <el-rate v-model="scope.row.difficulty" disabled />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default>
            <el-button link type="primary" size="small">编辑</el-button>
            <el-button link type="danger" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页组件 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>

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
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import { uploadRecipe, getRecipesList } from "@/api/recipe";

const tableData = ref([]); // 实际项目中此处应调用获取列表接口
const loading = ref(false);

const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

const dialogVisible = ref(false);
const uploading = ref(false);
const uploadForm = ref({
  category: "",
  mdFile: null as File | null,
  imageFile: null as File | null,
});

// 获取列表数据方法
const fetchRecipes = async () => {
  loading.value = true;
  try {
    const res = await getRecipesList(currentPage.value, pageSize.value);
    tableData.value = res.data.data;
    total.value = res.data.total;
  } catch (error) {
    ElMessage.error("获取菜谱列表失败");
  } finally {
    loading.value = false;
  }
};

// 分页触发事件
const handleSizeChange = (val: number) => {
  pageSize.value = val;
  fetchRecipes();
};

const handleCurrentChange = (val: number) => {
  currentPage.value = val;
  fetchRecipes();
};

// 页面挂载时初始化数据
onMounted(() => {
  fetchRecipes();
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
    ElMessage.success(res.data.message || "上传成功");
    dialogVisible.value = false;

    // 关键：上传成功后重新拉取第一页数据，展现刚插入的菜谱
    currentPage.value = 1;
    fetchRecipes();
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
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end; /* 将分页组件靠右对齐 */
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
