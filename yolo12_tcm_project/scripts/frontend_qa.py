from __future__ import annotations

import json
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
URL = "http://127.0.0.1:5173"
API_HEALTH_URL = "http://127.0.0.1:8000/health"
CLS_MODEL = ROOT / "runs" / "train" / "strict_classify_yolo12n_cls_cpu_5e" / "weights" / "best.pt"
CLS_IMAGE = ROOT / "data" / "classification_strict_jpeg" / "val" / "丝瓜络" / "Sigualuo117.jpg"


def get_backend_note() -> str:
    try:
        with urllib.request.urlopen(API_HEALTH_URL, timeout=2) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if payload.get("status") == "ok":
            return "- 说明: FastAPI 后端已连接，`/models` 和图片识别接口可用于联调。"
    except Exception as exc:
        return f"- 说明: FastAPI 后端未连接，前端应给出可理解的错误提示；检测到的问题为 {exc.__class__.__name__}。"
    return "- 说明: FastAPI 后端响应异常，前端应保持页面可用并提示接口状态。"


def run_viewport(page, name: str, width: int, height: int) -> dict:
    page.set_viewport_size({"width": width, "height": height})
    page.goto(URL, wait_until="networkidle")
    page.screenshot(path=str(ROOT / "reports" / "figures" / f"frontend_{name}.png"), full_page=True)
    body_text = page.locator("body").inner_text(timeout=5000)
    title = page.title()
    overlay = page.locator("text=/plugin-vue|Internal server error|Vite Error|Failed to resolve/").count()
    return {
        "viewport": name,
        "url": page.url,
        "title": title,
        "not_blank": "中药饮片识别" in body_text and "图片上传识别" in body_text,
        "framework_overlay_absent": overlay == 0,
        "body_excerpt": body_text[:300],
        "screenshot": str(ROOT / "reports" / "figures" / f"frontend_{name}.png"),
    }


def main() -> int:
    out_dir = ROOT / "reports" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    logs: list[dict] = []
    checks: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("console", lambda msg: logs.append({"type": msg.type, "text": msg.text}))
        page.on("pageerror", lambda exc: logs.append({"type": "pageerror", "text": str(exc)}))

        checks.append(run_viewport(page, "desktop", 1440, 900))

        classify_check = {
            "viewport": "desktop",
            "interaction": "classify_upload",
            "passed": False,
            "detail": "strict 分类样例未执行。",
        }
        if CLS_MODEL.exists() and CLS_IMAGE.exists():
            try:
                page.wait_for_function(
                    "(modelPath) => Array.from(document.querySelectorAll('select option')).some(option => option.value === modelPath)",
                    arg=str(CLS_MODEL),
                    timeout=8000,
                )
                page.locator("select").select_option(str(CLS_MODEL))
                page.locator("input[type=file]").set_input_files(str(CLS_IMAGE))
                page.get_by_role("button", name="开始识别").click()
                page.wait_for_selector("text=Top-1", timeout=30000)
                body_text = page.locator("body").inner_text(timeout=5000)
                page.screenshot(path=str(ROOT / "reports" / "figures" / "frontend_classify_result.png"), full_page=True)
                classify_check = {
                    "viewport": "desktop",
                    "interaction": "classify_upload",
                    "passed": "完成分类" in body_text and "Top-1" in body_text and "置信度" in body_text,
                    "detail": "上传 strict 验证图后返回分类 Top-k 结果。",
                    "screenshot": str(ROOT / "reports" / "figures" / "frontend_classify_result.png"),
                }
            except Exception as exc:
                classify_check = {
                    "viewport": "desktop",
                    "interaction": "classify_upload",
                    "passed": False,
                    "detail": f"分类上传流程失败：{exc.__class__.__name__}: {exc}",
                }
        checks.append(classify_check)

        page.get_by_role("button", name="目标检测").click()
        detect_text = page.locator("body").inner_text(timeout=5000)
        checks.append(
            {
                "viewport": "desktop",
                "interaction": "nav_detect",
                "passed": "目标检测识别" in detect_text and "检测模式返回边界框" in detect_text,
                "detail": "目标检测页签保留，可用于未来真实 bbox 权重。",
            }
        )

        page.get_by_role("button", name="摄像头").click()
        camera_text = page.locator("body").inner_text(timeout=5000)
        checks.append(
            {
                "viewport": "desktop",
                "interaction": "nav_camera",
                "passed": "摄像头截帧识别" in camera_text and "打开摄像头" in camera_text,
                "detail": "摄像头页签切换成功；未自动请求摄像头权限。",
            }
        )

        page.get_by_role("button", name="训练入口").click()
        train_text = page.locator("body").inner_text(timeout=5000)
        checks.append(
            {
                "viewport": "desktop",
                "interaction": "nav_train",
                "passed": "管理员训练入口" in train_text and "启动训练" in train_text,
                "detail": "训练页签切换成功。",
            }
        )

        checks.append(run_viewport(page, "mobile", 390, 844))
        browser.close()

    relevant_errors = [
        item
        for item in logs
        if item["type"] in {"error", "pageerror"}
        and "ERR_CONNECTION_REFUSED" not in item["text"]
        and "http://127.0.0.1:8000/models" not in item["text"]
    ]
    report = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "url": URL,
        "browser_path": "Playwright fallback; Browser plugin not available in this session.",
        "checks": checks,
        "console_logs": logs,
        "relevant_console_errors": relevant_errors,
        "summary": {
            "checks_total": len(checks),
            "checks_passed": sum(1 for c in checks if c.get("passed", c.get("not_blank", False) and c.get("framework_overlay_absent", False))),
            "relevant_console_errors": len(relevant_errors),
        },
    }
    (ROOT / "reports" / "frontend_qa.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 前端渲染 QA 报告",
        "",
        f"- 时间: {report['timestamp']}",
        f"- URL: {URL}",
        "- Browser 路径: Browser plugin not available，使用 Playwright fallback。",
        get_backend_note(),
        "",
        "## 检查结果",
        "",
        "| 检查 | 状态 | 说明 |",
        "|---|---|---|",
    ]
    for c in checks:
        if "interaction" in c:
            lines.append(f"| {c['interaction']} | {'通过' if c['passed'] else '未通过'} | {c['detail']} |")
        else:
            ok = c["not_blank"] and c["framework_overlay_absent"]
            lines.append(f"| {c['viewport']} 渲染 | {'通过' if ok else '未通过'} | title={c['title']}；screenshot={c['screenshot']} |")
    lines.extend(
        [
            "",
            "## 截图",
            "",
            f"- 桌面端: `{ROOT / 'reports' / 'figures' / 'frontend_desktop.png'}`",
            f"- 分类结果: `{ROOT / 'reports' / 'figures' / 'frontend_classify_result.png'}`",
            f"- 移动端: `{ROOT / 'reports' / 'figures' / 'frontend_mobile.png'}`",
        ]
    )
    (ROOT / "reports" / "frontend_qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
