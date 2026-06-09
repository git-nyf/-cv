# 环境说明

## 推荐环境

- Windows 11 或 Linux
- Python 3.10-3.12 优先。当前机器只有 Python 3.13 时，可先用于脚本和前端 QA；训练环境建议另装 3.11/3.12，以降低 PyTorch/Ultralytics 轮子兼容风险。
- NVIDIA GPU + CUDA，训练推荐 8 GB 以上显存；YOLOv12s/更高输入尺寸建议更高显存
- Node.js 18+

## Python 依赖

见 `requirements.txt`。核心依赖：

- `ultralytics`
- `torch`
- `opencv-python`
- `fastapi`
- `pillow`
- `pyyaml`
- `psutil`

## YOLOv12 代码入口

本工程默认采用 Ultralytics 的 YOLO12 接口作为训练、验证、推理和导出入口，原因是：

- API 覆盖训练、验证、推理、导出，便于课程复现。
- 与 YOLO 系列命令和数据格式保持一致。
- 后端服务可以直接加载 `.pt` 权重。

同时保留对 `sunsmarterjie/yolov12` 官方论文仓库的引用。若课程要求严格复现论文仓库，应在单独分支中记录仓库 commit、安装方式和训练命令。

## 风险

YOLOv12 是注意力中心的研究模型，可能出现：

- 训练稳定性弱于成熟 YOLOv8/YOLOv11。
- 显存占用较高。
- CPU 推理速度慢。
- 第三方库版本更新导致模型名或导出接口变化。

应先跑 YOLOv12n 的最小闭环，再扩展到 YOLOv12s 和调参实验。

## 当前机器提示

当前检测到 `py -0p` 只有 Python 3.13。若 `pip install torch ultralytics` 失败，建议安装 Python 3.11 或 3.12 后运行：

```powershell
.\scripts\setup_env.ps1 -Python "C:\Path\To\Python312\python.exe"
```
