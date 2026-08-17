<template>
  <div class="page-container">
    <div class="glass-panel content-wrapper">
      <h2>今日吃什么 ✨</h2>
      <p>不知道吃什么？来摇一摇获取灵感吧！</p>

      <div class="random-box">
        <el-button type="warning" size="large" round> 获取随机推荐 </el-button>
      </div>
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
.random-box {
  margin-top: 50px;
  display: flex;
  justify-content: center;
}
</style>
