<template>
  <div class="page-container">
    <div class="glass-panel content-wrapper">
      <div class="manage-header">
        <div>
          <h2>知识库管理</h2>
          <p>添加、编辑或删除菜谱与厨房技巧</p>
        </div>
        <el-button type="primary" round>添加新菜谱</el-button>
      </div>

      <el-table
        :data="[]"
        style="width: 100%; margin-top: 20px"
        empty-text="暂无数据"
      >
        <el-table-column prop="name" label="菜名/知识点" width="180" />
        <el-table-column prop="category" label="分类" width="120" />
        <el-table-column prop="difficulty" label="难度" />
        <el-table-column label="操作" width="150" />
      </el-table>
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-container {
  height: 100%;
}
.content-wrapper {
  padding: 30px;
  height: 100%;
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
}
p {
  color: #666;
  margin-bottom: 0;
}
</style>
