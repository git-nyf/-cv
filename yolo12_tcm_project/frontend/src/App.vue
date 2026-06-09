<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">Y12</div>
        <div>
          <h1>中药饮片识别</h1>
          <p>YOLOv12 Recognition Console</p>
        </div>
      </div>

      <nav class="nav">
        <button :class="{ active: view === 'classify' }" @click="switchView('classify')">
          <ScanSearch :size="18" /> 分类识别
        </button>
        <button :class="{ active: view === 'detect' }" @click="switchView('detect')">
          <ScanLine :size="18" /> 目标检测
        </button>
        <button :class="{ active: view === 'camera' }" @click="switchView('camera')">
          <Camera :size="18" /> 摄像头
        </button>
        <button :class="{ active: view === 'train' }" @click="switchView('train')">
          <Activity :size="18" /> 训练入口
        </button>
      </nav>

      <section v-if="view === 'classify' || view === 'detect'" class="side-section">
        <label>当前权重</label>
        <select v-model="selectedModel">
          <option value="">自动选择最新权重</option>
          <option v-for="model in models" :key="model.path" :value="model.path">
            {{ model.name }} · {{ model.modified_time }}
          </option>
        </select>
        <button class="secondary" @click="loadModels">
          <RefreshCw :size="16" /> 刷新权重
        </button>
      </section>

      <section class="side-section">
        <label>{{ view === 'detect' ? '检测阈值' : '分类输出' }}</label>
        <div v-if="view === 'detect'" class="control-row">
          <span>Conf</span>
          <input v-model.number="conf" type="range" min="0.05" max="0.9" step="0.05" />
          <strong>{{ conf.toFixed(2) }}</strong>
        </div>
        <div v-if="view === 'detect'" class="control-row">
          <span>IoU</span>
          <input v-model.number="iou" type="range" min="0.3" max="0.9" step="0.05" />
          <strong>{{ iou.toFixed(2) }}</strong>
        </div>
        <div v-else class="control-row">
          <span>TopK</span>
          <input v-model.number="topk" type="range" min="1" max="5" step="1" />
          <strong>{{ topk }}</strong>
        </div>
      </section>
    </aside>

    <main class="workspace">
      <header class="topbar">
        <div>
          <h2>{{ currentTitle }}</h2>
          <p>{{ status }}</p>
        </div>
        <a class="doc-link" :href="`${apiBase}/docs`" target="_blank">API Docs</a>
      </header>

      <section v-if="view === 'classify' || view === 'detect'" class="main-grid">
        <div class="panel upload-panel">
          <div class="dropzone" @dragover.prevent @drop.prevent="onDrop">
            <UploadCloud :size="38" />
            <h3>上传中药饮片图片</h3>
            <p>{{ view === 'detect' ? '检测模式返回边界框、类别与置信度。' : '分类模式返回 Top-k 类别与置信度。' }}</p>
            <input ref="fileInput" type="file" accept="image/*" @change="onFileChange" />
            <button @click="$refs.fileInput.click()">选择图片</button>
          </div>
          <button class="primary" :disabled="!imageFile || loading" @click="recognizeImage">
            <LoaderCircle v-if="loading" class="spin" :size="17" />
            <ScanSearch v-else :size="17" />
            开始识别
          </button>
        </div>

        <ResultPanel :preview-url="previewUrl" :result="result" :api-base="apiBase" :mode="view" />
      </section>

      <section v-else-if="view === 'camera'" class="panel camera-panel">
        <div class="camera-toolbar">
          <button class="primary" @click="toggleCamera">
            <Camera :size="17" /> {{ cameraActive ? '关闭摄像头' : '打开摄像头' }}
          </button>
          <button :disabled="!cameraActive || loading" @click="captureFrame">
            <ScanLine :size="17" /> 截帧识别
          </button>
        </div>
        <video ref="video" autoplay playsinline muted></video>
        <p class="hint">实时流部署可扩展为 WebSocket；课程演示版采用浏览器截帧上传，便于跨平台运行。</p>
      </section>

      <section v-else class="panel train-panel">
        <div class="form-grid">
          <label>
            训练配置
            <input v-model="trainConfig" />
          </label>
          <label>
            模型
            <input v-model="trainModel" placeholder="可空，使用配置文件" />
          </label>
          <label>
            Epochs
            <input v-model.number="trainEpochs" type="number" min="1" />
          </label>
          <label>
            Device
            <input v-model="trainDevice" placeholder="0 / cpu" />
          </label>
        </div>
        <button class="primary" @click="startTrain">
          <Play :size="17" /> 启动训练
        </button>
        <pre v-if="trainMessage">{{ trainMessage }}</pre>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import {
  Activity,
  Camera,
  LoaderCircle,
  Play,
  RefreshCw,
  ScanLine,
  ScanSearch,
  UploadCloud,
} from 'lucide-vue-next'
import ResultPanel from './components/ResultPanel.vue'

const apiBase = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
const view = ref('classify')
const status = ref('等待后端连接')
const models = ref([])
const selectedModel = ref('')
const conf = ref(0.25)
const iou = ref(0.7)
const topk = ref(5)
const imageFile = ref(null)
const previewUrl = ref('')
const result = ref(null)
const loading = ref(false)
const fileInput = ref(null)
const video = ref(null)
const cameraActive = ref(false)
const stream = ref(null)
const trainConfig = ref('configs/train_baseline.yaml')
const trainModel = ref('')
const trainEpochs = ref(20)
const trainDevice = ref('0')
const trainMessage = ref('')

const currentTitle = computed(() => ({
  classify: '图片上传识别',
  detect: '目标检测识别',
  camera: '摄像头截帧识别',
  train: '管理员训练入口',
}[view.value]))

function switchView(nextView) {
  if (view.value !== nextView) {
    result.value = null
  }
  view.value = nextView
}

async function loadModels() {
  try {
    const res = await fetch(`${apiBase}/models`)
    models.value = await res.json()
    status.value = models.value.length ? `发现 ${models.value.length} 个权重文件` : '未发现权重文件，请先训练或放入 best.pt'
  } catch (err) {
    status.value = `后端未连接：${err.message}`
  }
}

function setImage(file) {
  imageFile.value = file
  result.value = null
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
  previewUrl.value = URL.createObjectURL(file)
}

function onFileChange(event) {
  const file = event.target.files?.[0]
  if (file) setImage(file)
}

function onDrop(event) {
  const file = event.dataTransfer.files?.[0]
  if (file) setImage(file)
}

async function recognizeImage() {
  if (!imageFile.value) return
  loading.value = true
  status.value = view.value === 'detect' ? '正在检测' : '正在分类'
  const form = new FormData()
  form.append('file', imageFile.value)
  form.append('model', selectedModel.value)
  if (view.value === 'detect') {
    form.append('conf', conf.value)
    form.append('iou', iou.value)
    form.append('imgsz', 640)
  } else {
    form.append('topk', topk.value)
    form.append('imgsz', 224)
  }
  try {
    const endpoint = view.value === 'detect' ? 'detect/image' : 'classify/image'
    const res = await fetch(`${apiBase}/${endpoint}`, { method: 'POST', body: form })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || '识别失败')
    result.value = data
    status.value = view.value === 'detect'
      ? `完成检测：${data.detections.length} 个目标，${data.elapsed_ms.toFixed(1)} ms`
      : `完成分类：${data.top1_class_name || 'NA'}，${data.elapsed_ms.toFixed(1)} ms`
  } catch (err) {
    status.value = err.message
  } finally {
    loading.value = false
  }
}

async function toggleCamera() {
  if (cameraActive.value) {
    stream.value?.getTracks().forEach((track) => track.stop())
    cameraActive.value = false
    return
  }
  stream.value = await navigator.mediaDevices.getUserMedia({ video: true })
  video.value.srcObject = stream.value
  cameraActive.value = true
}

async function captureFrame() {
  const canvas = document.createElement('canvas')
  canvas.width = video.value.videoWidth
  canvas.height = video.value.videoHeight
  const ctx = canvas.getContext('2d')
  ctx.drawImage(video.value, 0, 0)
  canvas.toBlob((blob) => {
    if (!blob) return
    setImage(new File([blob], 'camera-frame.jpg', { type: 'image/jpeg' }))
    view.value = 'classify'
    recognizeImage()
  }, 'image/jpeg')
}

async function startTrain() {
  const payload = {
    config: trainConfig.value,
    model: trainModel.value || null,
    epochs: trainEpochs.value || null,
    device: trainDevice.value || null,
  }
  const res = await fetch(`${apiBase}/train/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  const data = await res.json()
  trainMessage.value = JSON.stringify(data, null, 2)
}

onMounted(loadModels)
</script>
