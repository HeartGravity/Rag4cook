<template>
  <div class="page-container">
    <div class="glass-panel content-wrapper">
      <h2>我的收藏 ❤️</h2>
      <p>你珍藏的绝密菜谱和厨房妙招都在这里。</p>
      <el-empty description="收藏夹还是空的，去看看有什么好吃的吧" />
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
