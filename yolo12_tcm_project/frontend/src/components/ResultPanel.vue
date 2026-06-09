<template>
  <div class="panel result-panel">
    <div class="panel-head">
      <div>
        <h3>识别结果</h3>
        <p v-if="result && mode === 'detect'">{{ result.detections?.length || 0 }} 个检测目标</p>
        <p v-else-if="result && mode === 'classify'">Top-1：{{ result.top1_class_name || 'NA' }}</p>
        <p v-else>上传图片后显示可视化结果和结构化 JSON。</p>
      </div>
      <a v-if="result?.saved_image" :href="`${apiBase}/files?path=${encodeURIComponent(result.saved_image)}`" target="_blank">
        打开结果图
      </a>
    </div>

    <div class="image-stage">
      <img v-if="result?.saved_image" :src="`${apiBase}/files?path=${encodeURIComponent(result.saved_image)}`" alt="检测结果" />
      <img v-else-if="previewUrl" :src="previewUrl" alt="上传预览" />
      <div v-else class="empty-state">暂无图片</div>
    </div>

    <table v-if="mode === 'classify' && result?.predictions?.length">
      <thead>
        <tr>
          <th>排序</th>
          <th>类别</th>
          <th>置信度</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, idx) in result.predictions" :key="idx">
          <td>Top-{{ idx + 1 }}</td>
          <td>{{ item.class_name }}</td>
          <td>{{ (item.confidence * 100).toFixed(1) }}%</td>
        </tr>
      </tbody>
    </table>

    <table v-else-if="result?.detections?.length">
      <thead>
        <tr>
          <th>类别</th>
          <th>置信度</th>
          <th>边界框 xyxy</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, idx) in result.detections || []" :key="idx">
          <td>{{ item.class_name }}</td>
          <td>{{ (item.confidence * 100).toFixed(1) }}%</td>
          <td>{{ item.bbox_xyxy.map(v => v.toFixed(1)).join(', ') }}</td>
        </tr>
      </tbody>
    </table>

    <pre v-if="result">{{ JSON.stringify(result, null, 2) }}</pre>
  </div>
</template>

<script setup>
defineProps({
  previewUrl: { type: String, default: '' },
  result: { type: Object, default: null },
  apiBase: { type: String, required: true },
  mode: { type: String, default: 'classify' },
})
</script>
