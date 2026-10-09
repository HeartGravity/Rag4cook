<!-- src/components/TipDetailModal.vue -->
<template>
  <el-dialog
    v-model="visible"
    width="680px"
    class="tip-detail-dialog"
    destroy-on-close
    append-to-body
    @close="handleClose"
  >
    <div v-loading="loading" class="tip-modal-body">
      <template v-if="tip">
        <!-- 弹窗顶栏 -->
        <div class="tip-header">
          <div class="badge-row">
            <span class="category-badge">💡 {{ tip.category }}</span>
            <el-tag
              v-if="tip.time_estimate"
              size="small"
              type="success"
              effect="plain"
              round
            >
              ⏱ 建议耗时: {{ tip.time_estimate }}
            </el-tag>
          </div>
          <h2 class="tip-title">{{ tip.name }}</h2>
          <div v-if="tip.tags?.length" class="tags-container">
            <span v-for="tag in tip.tags" :key="tag" class="tip-tag"
              >#{{ tag }}</span
            >
          </div>
        </div>

        <!-- 详细说明 -->
        <div v-if="tip.description" class="content-block intro-block">
          <p>{{ tip.description }}</p>
        </div>

        <!-- 技法要诀 -->
        <div v-if="tip.methods" class="content-block method-block">
          <div class="block-title">
            <el-icon><Operation /></el-icon> 核心技巧与要点
          </div>
          <div class="method-text">{{ tip.methods }}</div>
        </div>

        <!-- 所需厨具/辅料 -->
        <div v-if="tip.tools" class="content-block tools-block">
          <div class="block-title">
            <el-icon><Suitcase /></el-icon> 推荐使用工具与辅材
          </div>
          <div class="tools-text">{{ tip.tools }}</div>
        </div>

        <!-- 避坑与安全提示 (特别设计) -->
        <div v-if="tip.safety_warnings" class="content-block warning-block">
          <div class="warning-title">
            <el-icon><WarningFilled /></el-icon> 避坑预警与安全须知
          </div>
          <div class="warning-text">{{ tip.safety_warnings }}</div>
        </div>

        <!-- 关联图谱概念 -->
        <div
          v-if="tip.related_nodes?.length"
          class="content-block related-block"
        >
          <div class="block-title">
            <el-icon><Share /></el-icon> 关联图谱知识
          </div>
          <div class="related-tags">
            <el-tag
              v-for="rel in tip.related_nodes"
              :key="rel.id"
              size="small"
              class="rel-tag"
            >
              {{ rel.name }} ({{ rel.relation }})
            </el-tag>
          </div>
        </div>
      </template>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import {
  Operation,
  Suitcase,
  WarningFilled,
  Share,
} from "@element-plus/icons-vue";
import { getTipDetail } from "@/api/tip";

const props = defineProps<{
  modelValue: boolean;
  tipId: string | null;
}>();

const emit = defineEmits(["update:modelValue"]);

const visible = ref(props.modelValue);
const loading = ref(false);
const tip = ref<any>(null);

watch(
  () => props.modelValue,
  (val) => {
    visible.value = val;
    if (val && props.tipId) {
      loadDetail(props.tipId);
    }
  },
);

const loadDetail = async (id: string) => {
  loading.value = true;
  try {
    const res = await getTipDetail(id);
    tip.value = res.data;
  } catch (err) {
    console.error("加载技巧详情失败", err);
  } finally {
    loading.value = false;
  }
};

const handleClose = () => {
  emit("update:modelValue", false);
  tip.value = null;
};
</script>

<style lang="scss">
.tip-detail-dialog {
  border-radius: 20px !important;
  background: rgba(255, 253, 250, 0.96) !important;
  backdrop-filter: blur(20px);
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.16) !important;
  border: 1px solid rgba(247, 160, 114, 0.3) !important;
  overflow: hidden;

  .el-dialog__header {
    padding-bottom: 0;
  }
  .el-dialog__body {
    padding: 10px 30px 30px;
    max-height: 75vh;
    overflow-y: auto;
  }
}
</style>

<style scoped lang="scss">
.tip-modal-body {
  min-height: 180px;
}

.tip-header {
  border-bottom: 1px dashed rgba(247, 160, 114, 0.4);
  padding-bottom: 14px;
  margin-bottom: 16px;

  .badge-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;

    .category-badge {
      font-size: 13px;
      font-weight: 600;
      color: #e65100;
      background: #ffe0b2;
      padding: 3px 10px;
      border-radius: 12px;
    }
  }

  .tip-title {
    margin: 4px 0 10px;
    font-size: 24px;
    color: #2c3e50;
    line-height: 1.3;
  }

  .tags-container {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;

    .tip-tag {
      font-size: 12px;
      color: #9e9e9e;
    }
  }
}

.content-block {
  margin-bottom: 16px;
  border-radius: 12px;
  padding: 14px 18px;

  .block-title {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 15px;
    font-weight: 600;
    color: #444;
    margin-bottom: 8px;
  }
}

.intro-block {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid #f0f0f0;
  p {
    margin: 0;
    font-size: 14px;
    line-height: 1.7;
    color: #555;
  }
}

.method-block {
  background: #f1f8e9;
  border-left: 4px solid #7cb342;
  .method-text {
    font-size: 14px;
    line-height: 1.6;
    color: #33691e;
    white-space: pre-line;
  }
}

.tools-block {
  background: #ede7f6;
  border-left: 4px solid #7e57c2;
  .tools-text {
    font-size: 14px;
    line-height: 1.6;
    color: #4527a0;
  }
}

.warning-block {
  background: #fff3e0;
  border: 1px solid #ffcc80;
  border-left: 4px solid #ff9800;

  .warning-title {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 15px;
    font-weight: 600;
    color: #e65100;
    margin-bottom: 6px;
  }

  .warning-text {
    font-size: 14px;
    line-height: 1.6;
    color: #bf360c;
  }
}

.related-block {
  background: #f5f5f5;
  .related-tags {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    .rel-tag {
      background: #fff;
    }
  }
}
</style>
