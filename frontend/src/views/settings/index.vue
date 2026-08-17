<template>
  <div class="page-container">
    <div class="glass-panel content-wrapper">
      <h2>系统设置 ⚙️</h2>
      <p>配置后端服务接口与偏好设置</p>

      <el-form label-width="120px" class="settings-form">
        <el-form-item label="后端 API 地址">
          <el-input placeholder="例如：http://localhost:8000" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary">保存配置</el-button>
        </el-form-item>
      </el-form>
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
  margin-bottom: 30px;
}
.settings-form {
  max-width: 500px;
}
</style>
