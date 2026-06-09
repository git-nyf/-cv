# 前端渲染 QA 报告

- 时间: 2026-06-07T01:32:44
- URL: http://127.0.0.1:5173
- Browser 路径: Browser plugin not available，使用 Playwright fallback。
- 说明: FastAPI 后端已连接，`/models` 和图片识别接口可用于联调。

## 检查结果

| 检查 | 状态 | 说明 |
|---|---|---|
| desktop 渲染 | 通过 | title=YOLOv12 中药饮片识别系统；screenshot=D:\AAA中药cv\yolo12_tcm_project\reports\figures\frontend_desktop.png |
| classify_upload | 通过 | 上传 strict 验证图后返回分类 Top-k 结果。 |
| nav_detect | 通过 | 目标检测页签保留，可用于未来真实 bbox 权重。 |
| nav_camera | 通过 | 摄像头页签切换成功；未自动请求摄像头权限。 |
| nav_train | 通过 | 训练页签切换成功。 |
| mobile 渲染 | 通过 | title=YOLOv12 中药饮片识别系统；screenshot=D:\AAA中药cv\yolo12_tcm_project\reports\figures\frontend_mobile.png |

## 截图

- 桌面端: `D:\AAA中药cv\yolo12_tcm_project\reports\figures\frontend_desktop.png`
- 分类结果: `D:\AAA中药cv\yolo12_tcm_project\reports\figures\frontend_classify_result.png`
- 移动端: `D:\AAA中药cv\yolo12_tcm_project\reports\figures\frontend_mobile.png`
