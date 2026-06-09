# 使用说明

本文档说明如何启动、使用和测试 `yolo12_tcm_project`。当前系统主线是中药饮片图片分类识别；检测入口已保留，但真实 bbox 标注尚未完成，因此不要把当前结果当作目标检测 mAP、Precision 或 Recall。

## 1. 项目位置

```text
D:\AAA中药cv\yolo12_tcm_project
```

原始数据位置：

```text
D:\AAA中药cv\data
```

推荐测试图片位置：

```text
D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\<类别>\*.jpg
```

## 2. 首次环境准备

打开 PowerShell：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\scripts\setup_env.ps1
```

如需手动激活 Python 环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

## 3. 启动系统

需要两个 PowerShell 窗口。

第一个窗口启动后端：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\scripts\start_backend.ps1
```

后端地址：

```text
http://127.0.0.1:8000
```

API 文档：

```text
http://127.0.0.1:8000/docs
```

第二个窗口启动前端：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\scripts\start_frontend.ps1
```

前端地址：

```text
http://127.0.0.1:5173
```

### 3.1 命令行直接启动

如果不想用 VSCode 任务，也可以直接开两个命令行窗口运行。

第一个窗口启动后端：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

第二个窗口启动前端：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project\frontend
npm run dev
```

然后打开前端页面：

```text
http://127.0.0.1:5173
```

说明：当前前端支持 `npm run dev`，后端用 Python/uvicorn 启动；项目根目录暂时没有一个统一的 `npm start` 同时启动前后端。

### 3.2 PyCharm 启动后端

后端已经提供 IDE 可执行入口：

```text
D:\AAA中药cv\yolo12_tcm_project\backend\run.py
```

在 PyCharm 中操作：

1. 打开项目目录 `D:\AAA中药cv\yolo12_tcm_project`。
2. 打开 `backend/run.py`。
3. 在 `if __name__ == "__main__":` 左侧点击绿色三角形。
4. 选择 `Run 'run'`。

启动成功后访问：

```text
http://127.0.0.1:8000/docs
```

这个入口等价于命令行启动：

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

说明：`backend/run.py` 会自动把项目根目录加入 Python 搜索路径，因此即使 PyCharm 的工作目录设置不同，也能稳定找到 `backend.app.main:app`。

## 4. 前端分类识别操作

1. 打开浏览器访问 `http://127.0.0.1:5173`。
2. 左侧选择“分类识别”。
3. 在“当前权重”下拉框中选择最新 GPU 100 epoch 模型：

```text
runs\train\strict_classify_yolo12n_cls_gpu_100e\weights\best.pt
```

如果不手动选择，后端通常会按修改时间自动选最新 `.pt`，当前最新模型也应是上面的 GPU 100 epoch 模型。

4. 点击“选择图片”，推荐从这里选验证图片：

```text
D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val\<类别>\*.jpg
```

5. 点击“开始识别”。
6. 页面会显示 Top-k 分类结果、置信度和推理耗时。

## 5. 当前最佳模型

当前推荐分类模型：

```text
D:\AAA中药cv\yolo12_tcm_project\runs\train\strict_classify_yolo12n_cls_gpu_100e\weights\best.pt
```

训练配置：

```text
D:\AAA中药cv\yolo12_tcm_project\configs\train_cls_strict_gpu_100e.yaml
```

关键配置：

```yaml
epochs: 100
batch: 64
imgsz: 224
device: 0
pretrained: true
patience: 20
optimizer: AdamW
```

独立验证指标：

```text
Top-1: 0.6295
Top-5: 0.8621
Fitness: 0.7458
```

指标文件：

```text
D:\AAA中药cv\yolo12_tcm_project\reports\strict_classification_gpu_100e_evaluation_metrics.json
```

## 6. 后端接口快速测试

健康检查：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

正常应返回：

```json
{"status":"ok","service":"yolo12-tcm-api"}
```

查看模型列表：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/models
```

自动后端 QA：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\backend_qa.py
```

## 7. 前端测试

前端构建测试：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project\frontend
npm run build
```

前端 Playwright QA 需要先启动后端和前端：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\frontend_qa.py
```

完整工程自检：

```powershell
cd D:\AAA中药cv\yolo12_tcm_project
.\.venv\Scripts\python.exe scripts\smoke_check.py --output reports\smoke_check.json
```

历史通过标准：

```text
total=161, passed=161, failed=0
```

注意：如果训练配置或模型指标已更新，而 smoke 里仍有旧指标断言，需要同步更新 smoke 检查口径后再作为最终交付自检。

## 8. 在 VSCode 中训练

本项目已提供 VSCode 任务配置：

```text
D:\AAA中药cv\yolo12_tcm_project\.vscode\tasks.json
```

因此训练时不需要手动输入命令，只要在 VSCode 里选择任务运行。

### 8.1 打开项目

1. 打开 VSCode。
2. 点击菜单 `文件 -> 打开文件夹...`。
3. 选择项目文件夹：

```text
D:\AAA中药cv\yolo12_tcm_project
```

4. 等 VSCode 加载完成。

注意：一定要打开 `yolo12_tcm_project` 这个文件夹，不要只打开单个 `.py` 文件，也不要只打开上一级 `D:\AAA中药cv`。VSCode 任务依赖 `${workspaceFolder}`，打开错目录会找不到脚本和虚拟环境。

### 8.2 启动前后端

在 VSCode 中：

1. 按 `Ctrl + Shift + P`。
2. 输入并选择 `Tasks: Run Task`。
3. 选择 `启动后端 API`。
4. 再次按 `Ctrl + Shift + P`，选择 `Tasks: Run Task`。
5. 选择 `启动前端页面`。

启动后访问：

```text
http://127.0.0.1:5173
```

API 文档：

```text
http://127.0.0.1:8000/docs
```

### 8.3 训练分类模型

有 GPU 时选择：

```text
训练分类模型 GPU 100e
```

纯 CPU 时选择：

```text
训练分类模型 CPU 30e
```

操作步骤：

1. 按 `Ctrl + Shift + P`。
2. 输入并选择 `Tasks: Run Task`。
3. 选择 `训练分类模型 GPU 100e`。
4. VSCode 会自动打开任务输出窗口。
5. 等训练结束。

GPU 100e 训练使用的配置文件是：

```text
configs\train_cls_strict_gpu_100e.yaml
```

当前关键超参数：

```yaml
model: yolo12n-cls.yaml
data: data/classification_strict_jpeg
epochs: 100
batch: 64
imgsz: 224
optimizer: AdamW
lr0: 0.001
weight_decay: 0.0005
patience: 20
device: 0
workers: 4
pretrained: true
cache: false
plots: true
save: true
```

我实际修改过的关键超参数是：

```yaml
pretrained: false -> true
```

也就是说，这次没有换大模型，没有改图片尺寸，没有改学习率，主要改变是启用预训练，并用 GPU 跑满 100 epoch。

训练完成后的最佳模型位置：

```text
runs\train\strict_classify_yolo12n_cls_gpu_100e\weights\best.pt
```

### 8.4 评估训练结果

训练完成后，在 VSCode 里继续运行任务：

```text
评估 GPU 100e 分类模型
```

操作步骤：

1. 按 `Ctrl + Shift + P`。
2. 选择 `Tasks: Run Task`。
3. 选择 `评估 GPU 100e 分类模型`。

评估结果会写入：

```text
reports\strict_classification_gpu_100e_evaluation_metrics.json
```

当前已完成的一次 GPU 100 epoch 训练结果：

```text
Top-1: 0.6295
Top-5: 0.8621
Fitness: 0.7458
```

### 8.5 其他可用 VSCode 任务

可在 `Tasks: Run Task` 中选择：

```text
启动后端 API
启动前端页面
训练分类模型 GPU 100e
训练分类模型 CPU 30e
评估 GPU 100e 分类模型
后端 QA
前端构建测试
完整 smoke 自检
```

说明：VSCode 任务底层仍会调用 Python、npm 或 PowerShell，但你不需要手动输入命令，只需要在 VSCode 菜单里选择任务。

## 9. 检测功能边界

前端有“目标检测”入口，后端也有 `/detect/image` 接口，但当前真实数据没有 bbox 标注。

当前检测标注准备包：

```text
D:\AAA中药cv\yolo12_tcm_project\data\detection_annotation_package
```

状态：

```text
pending_bbox_annotation
```

含义：

- 图片准备好了。
- 类别顺序和 manifest 准备好了。
- `labels/` 仍为空。
- 不能直接训练真实检测模型。
- 不能汇报检测 mAP、Precision、Recall。

人工完成 YOLO bbox 标注后，再运行严格校验：

```powershell
.\.venv\Scripts\python.exe scripts\validate_detection_annotation_package.py --package data\detection_annotation_package --require-complete --output reports\detection_annotation_package_validation.json --markdown reports\detection_annotation_package_validation.md
```

## 10. 数据质量待处理项

当前仍有 34 组跨类别 exact duplicate 等待人工决策：

```text
D:\AAA中药cv\yolo12_tcm_project\reports\classification_cross_class_decision_table.csv
```

辅助查看页面：

```text
D:\AAA中药cv\yolo12_tcm_project\reports\classification_cross_class_decision_review.html
```

不要自动填写这个 CSV。需要人工确认真实类别后，再生成清理计划：

```powershell
.\.venv\Scripts\python.exe scripts\generate_classification_cross_class_cleanup_plan.py --decision-table reports\classification_cross_class_decision_table.json --decision-csv reports\classification_cross_class_decision_table.csv --output reports\classification_cross_class_cleanup_plan.json --operations-csv reports\classification_cross_class_cleanup_plan.csv --markdown reports\classification_cross_class_cleanup_plan.md
```

只有当清理计划状态为 `ready_for_cleanup_execution` 且 `validation_errors=0` 时，才允许执行非破坏性清理。

## 11. 常见问题

### 前端识别置信度很低怎么办？

先确认选择的是：

```text
strict_classify_yolo12n_cls_gpu_100e\weights\best.pt
```

不要选旧的 CPU 5 epoch 模型，也不要选 93 类 1 epoch 冒烟模型。

### 可以用原始 `D:\AAA中药cv\data\val` 测吗？

可以尝试，但推荐用清洗后的：

```text
D:\AAA中药cv\yolo12_tcm_project\data\classification_strict_jpeg\val
```

因为训练、验证和类别顺序都基于这个 strict JPEG 数据集。

### 为什么有些验证图仍然识别错？

当前最佳 Top-1 约 63%，不是 100%。它已经比 5 epoch CPU 模型明显好，但仍会错一些难样本。后续若继续提升，可尝试：

- `yolo12s-cls`
- `imgsz: 320` 或 `384`
- 完成 34 组跨类别标签冲突清理后重新训练

### 前端打不开怎么办？

检查两个端口：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
curl.exe -I http://127.0.0.1:5173
```

如果后端不通，重新运行：

```powershell
.\scripts\start_backend.ps1
```

如果前端不通，重新运行：

```powershell
.\scripts\start_frontend.ps1
```
