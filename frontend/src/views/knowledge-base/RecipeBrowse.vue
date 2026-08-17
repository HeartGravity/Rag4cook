<template>
  <div class="page-container">
    <div class="glass-panel content-wrapper">
      <h2>菜谱与知识库</h2>
      <p>在这里按分类检索你存入的菜谱和厨房技巧。</p>
      <el-empty description="知识库接口尚未接入，暂无数据" />
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
h2 {
  color: var(--primary-color);
  margin-top: 0;
}
p {
  color: #666;
}
</style>
