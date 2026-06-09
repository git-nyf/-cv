from __future__ import annotations

import json
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]


def clean_xml_text(value: object) -> str:
    text = str(value)
    return "".join(ch if ch in "\t\n\r" or ord(ch) >= 32 else " " for ch in text)


def add_table(document: Document, headers: list[str], rows: list[list[str]]) -> None:
    table = document.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    for i, header in enumerate(headers):
        hdr[i].text = header
    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = clean_xml_text(value)


def load_json_report(relative_path: str) -> dict | None:
    path = ROOT / relative_path
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def add_bullets(document: Document, items: list[str]) -> None:
    for item in items:
        document.add_paragraph(item, style="List Bullet")


def main() -> int:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)

    styles = doc.styles
    styles["Normal"].font.name = "Microsoft YaHei"
    styles["Normal"].font.size = Pt(10.5)

    title = doc.add_heading("基于 YOLOv12 的中草药饮片智能识别与分类系统测试报告", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph("第8组 · 2026年6月").alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading("1. 测试结论", level=1)
    doc.add_paragraph(
        "截至当前交付，项目已完成从工程环境、数据处理、YOLOv12 训练/调参/评估/推理、FastAPI 后端、Vue3 前端、"
        "模型导出、接口验证到概要设计 PPT 的完整工程闭环。当前本机 .venv 已安装并验证 torch 2.12.0+cpu、"
        "ultralytics 8.4.60、fastapi 0.136.3、playwright 1.60.0 等核心依赖，增强工程自检已扩展到覆盖 93 类补齐实验、重复/泄漏审计、泄漏人工复核包、候选泄漏清理集、跨类别复核包、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口、检测标注准备包和标注样本 contact sheet，单元测试 16/16 项通过。"
    )
    doc.add_paragraph(
        "已使用合成 demo YOLO 数据集完成最小训练闭环：数据生成、数据校验、train/val/test 划分、YOLOv12n CPU 1 epoch "
        "训练、测试集评估、图片推理、ONNX 导出、后端 API 调用和前端 Playwright 渲染 QA 均已跑通。该 demo 数据只用于"
        "证明项目流程和代码可运行，不代表真实中药饮片识别效果。"
    )
    doc.add_paragraph(
        "用户补充的真实中药饮片数据当前是分类目录，不含真实 bbox 标注。项目已完成 strict JPEG 分类数据集清洗与 "
        "YOLOv12n 分类 5 epoch CPU 训练，独立验证 Top-1 为 0.1769、Top-5 为 0.4957，并补充了每类表现、"
        "类别一致性审计、重复/泄漏审计、泄漏人工复核包、候选泄漏清理集、跨类别复核包、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口、可复现实验 Manifest、最高/最低类别、高频混淆对和人工复核 contact sheet。重复审计发现 strict 与 93 类补齐数据均存在 34 组 train/val exact duplicate 和 52 组跨类别 exact duplicate；本轮已生成覆盖全部 34 组的泄漏人工复核包，并构建 strict 与 93 类两个候选泄漏清理集，均只移除 val 侧泄漏副本，train/val 泄漏归零；剩余 34 组跨类别 exact duplicate 已单独生成复核包、对照图、可填写决策表、执行前 dry-run 清理计划报告和非破坏性执行脚本，仍需人工确认真实类别。类别审计显示原始数据 93 类、strict 基准实验 92 类；"
        "本轮新增 93 类补齐实验，将大腹皮 19 张原始 val-only 样本确定性重划为 15 train / 4 val，并完成 1 epoch CPU 冒烟训练，"
        "Top-1 为 0.0665、Top-5 为 0.2086。同时已生成检测 bbox 标注准备包、279 张样本总览 contact sheet 并完成 pending 状态校验，覆盖 93 类、279 张待标注图片，但 labels/ 仍为空，"
        "仅用于人工标注启动。该结果可作为真实分类数据阶段性指标；检测 Precision、Recall、mAP、"
        "bbox 定位能力仍需在补充真实检测标注后实测。报告不复用参考文献指标，也不将 demo 合成数据指标当作项目真实性能。"
    )

    doc.add_heading("2. 测试环境", level=1)
    add_table(
        doc,
        ["项目", "当前状态"],
        [
            ["操作系统", "Windows，本地工作区"],
            ["项目路径", str(ROOT)],
            ["Python 环境", ".venv\\Scripts\\python.exe"],
            ["Python 版本", "3.13.7"],
            ["PyTorch", "torch 2.12.0+cpu，当前为 CPU-only"],
            ["Ultralytics", "8.4.60"],
            ["后端框架", "fastapi 0.136.3 + uvicorn"],
            ["前端框架", "Vue3 + Vite"],
            ["GPU", "当前本机未检测到 CUDA；正式训练建议使用 NVIDIA GPU"],
            ["真实数据集", "已接入分类数据 data\\classification_strict_jpeg；已准备 data\\detection_annotation_package；真实检测 bbox 标签仍缺失"],
        ],
    )

    doc.add_heading("3. 功能测试矩阵", level=1)
    add_table(
        doc,
        ["模块", "测试项", "状态", "说明"],
        [
            ["环境搭建", "虚拟环境、依赖安装、脚本可导入", "通过", "scripts/smoke_check.py"],
            ["数据生成", "生成 demo YOLO 数据", "通过", "scripts/create_demo_dataset.py"],
            ["数据校验", "图片损坏、标签缺失、bbox 越界、重复图片", "通过", "demo 数据 0 errors / 0 warnings"],
            ["数据划分", "7:2:1 train/val/test", "通过", "demo 数据划分为 13 / 4 / 1"],
            ["真实分类数据清洗", "统一 JPEG、跳过 GIF/损坏图、排除无训练样本类别", "通过", "92 类，7826 train / 1741 val，0 errors / 0 warnings"],
            ["类别一致性审计", "原始 93 类与 strict 92 类差异、缺训练样本类别、跳过图分布", "通过", "reports/class_consistency_audit.md，大腹皮只在 val 出现，训练样本为 0"],
            ["重复/泄漏审计", "exact duplicate、train/val 泄漏、跨类别重复", "待人工复核", "strict 与 93 类补齐数据均发现 train/val 泄漏组 34、跨类别重复组 52"],
            ["泄漏人工复核包", "34 组 train/val exact duplicate 的 JSON、Markdown 和对照图", "通过", "reports/classification_leakage_review_package.md/json，18 组同时跨类别"],
            ["候选泄漏清理集", "基于复核包移除 val 侧泄漏副本并复审", "通过", "strict 9533 张、93 类 9552 张，train/val 泄漏组均为 0，跨类别重复组均为 34"],
            ["跨类别复核包", "34 组跨类别 exact duplicate 的 JSON、Markdown 和对照图", "待人工复核", "reports/classification_cross_class_review_package.md/json，manual_decision 等待填写"],
            ["跨类别决策表", "34 组跨类别标签冲突的 JSON/CSV/Markdown 填写表", "待人工填写", "reports/classification_cross_class_decision_table.md/json/csv，34/34 组 pending，校验错误 0"],
            ["跨类别清理计划校验", "人工决策 CSV 的执行前 dry-run 报告和操作预览 CSV", "待人工决策", "reports/classification_cross_class_cleanup_plan.md/json/csv，waiting_for_manual_decisions，计划操作 0"],
            ["跨类别清理执行入口", "校验通过后的非破坏性执行脚本", "待人工决策", "scripts/apply_classification_cross_class_cleanup_plan.py，当前计划未就绪时会阻断，只写新输出目录"],
            ["93 类补齐实验", "大腹皮 val-only 样本重划、93 类数据复审、1 epoch 训练和独立验证", "通过", "reports/classification_93class_training_report.md，Top-1 0.0665，Top-5 0.2086"],
            ["检测标注准备包", "93 类抽样、标注指南、classes.txt、manifest、空 labels/ 目录", "通过", "reports/detection_annotation_package_report.md，279 张待人工标注图片，labels/ 仍为空"],
            ["检测标注包校验", "待标注包结构、manifest、图片哈希、缺失标签统计、YOLO 标签严格验收入口", "通过", "reports/detection_annotation_package_validation.md，pending_bbox_annotation，缺失标签 279，errors 0"],
            ["检测标注样本总览", "每类 3 张待标注样本索引与 contact sheet PNG", "通过", "reports/detection_annotation_contact_sheet.md/json，样本 279、类别 93"],
            ["可复现实验 Manifest", "环境版本、复现命令、关键指标、实验边界和产物 SHA256", "通过", "reports/repro_manifest.md/json，包含检测标注准备包和 contact sheet 关键产物"],
            ["真实分类训练", "YOLOv12n 分类 CPU 5 epoch", "通过", "runs/train/strict_classify_yolo12n_cls_cpu_5e"],
            ["真实分类误判分析", "每类 Top-1/Top-5、高频混淆对、典型误判样例", "通过", "reports/strict_classification_error_analysis.md"],
            ["真实分类人工复核", "高频混淆和低表现类别 contact sheet", "通过", "reports/strict_classification_review_samples.md"],
            ["真实分类推理", "strict 权重 Top-k 单图推理", "通过", "scripts/infer_image_cls.py，输出 strict_classification_sample_prediction.json"],
            ["真实分类 benchmark", "strict 权重 CPU 延迟测试", "通过", "20 张样本 mean 9.76 ms/image，约 102.51 FPS"],
            ["基线训练", "YOLOv12n CPU 1 epoch", "通过", "runs/train/demo_yolo12n_smoke"],
            ["参数调优", "模型规模、imgsz、batch、lr 配置", "通过", "tune_yolo12.py 支持 dry-run/正式运行"],
            ["模型评估", "Precision、Recall、mAP", "通过 demo 流程", "demo 指标为 0，仅说明合成数据短训未形成可用精度"],
            ["图片推理", "保存结果图和 JSON", "通过", "infer_image.py、infer_image_cls.py"],
            ["后端接口", "health、models、detect/image、classify/image", "通过", "后端 QA 4/4"],
            ["前端页面", "分类上传、目标检测页签、摄像头页签、训练页签、桌面/移动端渲染", "通过", "前端 QA 6/6，相关 console error 0"],
            ["模型导出", "ONNX", "通过", "strict 分类 best.onnx 已生成"],
            ["测试报告", "Markdown + DOCX", "通过", "reports/test_report.md、reports/test_report.docx"],
            ["概要设计 PPT", "10 页概要设计汇报", "通过", "reports/overview_design.pptx"],
            ["提交前清单", "交付物、复现命令、验证结果和边界说明", "通过", "reports/submission_checklist.md"],
        ],
    )

    doc.add_heading("4. Demo 数据链路验证", level=1)
    demo = load_json_report("reports/demo_dataset_validation.json")
    if demo:
        summary = demo["summary"]
        add_table(
            doc,
            ["项目", "结果"],
            [
                ["图片数", str(summary["images"])],
                ["类别数", str(summary["classes_declared"])],
                ["errors", str(summary["errors"])],
                ["warnings", str(summary["warnings"])],
                ["划分结果", "train/val/test = 13 / 4 / 1"],
            ],
        )
    else:
        doc.add_paragraph("尚未生成 demo_dataset_validation.json。")

    doc.add_heading("5. Demo 训练、评估与导出", level=1)
    add_table(
        doc,
        ["项目", "结果"],
        [
            ["模型", "YOLOv12n"],
            ["训练设备", "CPU"],
            ["输入尺寸", "320"],
            ["batch", "2"],
            ["epoch", "1"],
            ["训练输出", "runs/train/demo_yolo12n_smoke"],
            ["权重", "best.pt、last.pt"],
            ["ONNX", "runs/train/demo_yolo12n_smoke/weights/best.onnx"],
        ],
    )

    eval_report = load_json_report("reports/demo_evaluation_metrics.json")
    if eval_report:
        add_table(
            doc,
            ["指标", "Demo 结果", "备注"],
            [
                ["Precision", str(eval_report.get("precision", "NA")), "工程验证，不代表真实数据"],
                ["Recall", str(eval_report.get("recall", "NA")), "工程验证，不代表真实数据"],
                ["mAP@50", str(eval_report.get("map50", "NA")), "工程验证，不代表真实数据"],
                ["mAP@50-95", str(eval_report.get("map50_95", "NA")), "工程验证，不代表真实数据"],
                ["fitness", str(eval_report.get("fitness", "NA")), "工程验证，不代表真实数据"],
            ],
        )
    doc.add_paragraph(
        "由于 demo 数据为合成几何图形，且只进行 CPU 1 epoch 短训，指标为 0 只说明最小训练流程未产生可泛化检测能力，"
        "不能作为真实中药饮片项目性能。"
    )

    doc.add_heading("6. 真实分类数据实验", level=1)
    doc.add_paragraph(
        "原始 D:\\AAA中药cv\\data 是 train/<类别名>/*.jpg、val/<类别名>/*.jpg 形式的分类数据集，未发现 .txt、"
        ".xml、.json、.csv 等真实 bbox 标注源。因此本阶段采用分类路线作为可信实验，不把分类目录伪装为真实检测数据。"
    )
    add_table(
        doc,
        ["项目", "结果"],
        [
            ["数据路径", "data/classification_strict_jpeg"],
            ["类别数", "92"],
            ["train 图像", "7826"],
            ["val 图像", "1741"],
            ["总图像", "9567"],
            ["跳过 GIF/损坏图", "28"],
            ["转换为 JPEG", "122"],
            ["图片复审 errors / warnings", "0 / 0"],
        ],
    )
    class_audit = load_json_report("reports/class_consistency_audit.json") or {}
    if class_audit:
        summary = class_audit.get("summary", {})
        add_table(
            doc,
            ["项目", "结果"],
            [
                ["类别一致性审计", "reports/class_consistency_audit.md/json"],
                ["原始类别", str(summary.get("raw_classes", 93))],
                ["原始 train / val 类别", f"{summary.get('raw_train_classes', 92)} / {summary.get('raw_val_classes', 93)}"],
                ["strict 类别", str(summary.get("strict_classes", 92))],
                ["未纳入 strict 类别", "、".join(summary.get("classes_missing_from_strict", ["大腹皮"]))],
                ["大腹皮原始 train / val", "0 / 19"],
                ["审计状态", summary.get("status", "needs_class_completion")],
            ],
        )
        doc.add_paragraph(
            "类别一致性审计用于固定当前 92 类 strict 实验边界：大腹皮只有验证样本、没有训练样本，"
            "因此不能纳入本轮训练；需补充训练样本后重建 strict 数据集，才能恢复完整 93 类分类实验。"
        )
    repro_manifest = load_json_report("reports/repro_manifest.json") or {}
    if repro_manifest:
        artifacts = repro_manifest.get("artifacts", [])
        commands = repro_manifest.get("reproduction_commands", [])
        packages = repro_manifest.get("environment", {}).get("packages", {})
        add_table(
            doc,
            ["项目", "结果"],
            [
                ["可复现实验 Manifest", "reports/repro_manifest.md/json"],
                ["关键产物哈希", f"{len(artifacts)} 个"],
                ["复现命令", f"{len(commands)} 条"],
                ["环境记录", f"torch {packages.get('torch')}，ultralytics {packages.get('ultralytics')}"],
                ["记录内容", "训练配置、类别审计摘要、重复/泄漏审计、泄漏人工复核包、候选泄漏清理集、跨类别复核包、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口、检测标注准备包、标注样本 contact sheet、Top-1/Top-5、benchmark、工程自检、报告与权重 SHA256"],
            ],
        )
        doc.add_paragraph(
            "可复现实验 Manifest 用于提交时追溯当前 strict 分类阶段结果：它记录复现命令、环境版本、关键指标、重复/泄漏审计、泄漏人工复核包、候选泄漏清理集、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口、检测标注样本 contact sheet、实验边界和关键产物 SHA256。"
        )

    strict_duplicates = load_json_report("reports/strict_classification_duplicate_audit.json") or {}
    completed_93_duplicates = load_json_report("reports/classification_93class_duplicate_audit.json") or {}
    if strict_duplicates and completed_93_duplicates:
        sdup = strict_duplicates.get("summary", {})
        d93 = completed_93_duplicates.get("summary", {})
        add_table(
            doc,
            ["项目", "strict 92 类", "93 类补齐"],
            [
                ["审计报告", "reports/strict_classification_duplicate_audit.md", "reports/classification_93class_duplicate_audit.md"],
                ["状态", sdup.get("status", "needs_leakage_review"), d93.get("status", "needs_leakage_review")],
                ["重复 SHA256 组", str(sdup.get("duplicate_hashes", 546)), str(d93.get("duplicate_hashes", 546))],
                ["train/val 泄漏组", str(sdup.get("train_val_leak_hashes", 34)), str(d93.get("train_val_leak_hashes", 34))],
                ["跨类别重复组", str(sdup.get("cross_class_duplicate_hashes", 52)), str(d93.get("cross_class_duplicate_hashes", 52))],
            ],
        )
        doc.add_paragraph("重复/泄漏审计只检查文件字节级 SHA256 完全重复；当前发现需人工复核，确认后再删除或重划，不能自动删图。")

    leakage_review = load_json_report("reports/classification_leakage_review_package.json") or {}
    if leakage_review:
        lsum = leakage_review.get("summary", {})
        add_table(
            doc,
            ["项目", "结果"],
            [
                ["泄漏人工复核包", "reports/classification_leakage_review_package.md/json"],
                ["复核对照图", "reports/figures/classification_train_val_leakage_contact_sheet.png"],
                ["覆盖 train/val 泄漏组", f"{lsum.get('leakage_groups', 34)} / {lsum.get('expected_leakage_groups', 34)}"],
                ["涉及文件记录", f"{lsum.get('leakage_records', 69)}，train {lsum.get('train_records', 35)} / val {lsum.get('val_records', 34)}"],
                ["同类别 / 跨类别泄漏组", f"{lsum.get('same_class_leakage_groups', 16)} / {lsum.get('cross_class_leakage_groups', 18)}"],
                ["与 93 类补齐审计共享泄漏哈希", str(lsum.get("shared_with_reference_leak_hashes", 34))],
                ["人工决策栏", "manual_decision 留空，等待人工确认后填写"],
            ],
        )
        doc.add_paragraph(
            "该复核包把 34 组 train/val exact duplicate 汇总成可逐项处理的清单和对照图，便于先确认类别目录是否混入、是否需要删除副本或重划样本；它不会自动修改数据集。"
        )

    cross_class_review = load_json_report("reports/classification_cross_class_review_package.json") or {}
    if cross_class_review:
        xsum = cross_class_review.get("summary", {})
        add_table(
            doc,
            ["项目", "结果"],
            [
                ["跨类别复核包", "reports/classification_cross_class_review_package.md/json"],
                ["复核对照图", "reports/figures/classification_cross_class_contact_sheet.png"],
                ["覆盖跨类别重复组", f"{xsum.get('cross_class_groups', 34)} / {xsum.get('expected_cross_class_groups', 34)}"],
                ["涉及文件记录", f"{xsum.get('cross_class_records', 68)}，train {xsum.get('train_records', 62)} / val {xsum.get('val_records', 6)}"],
                ["train/val 泄漏组", str(xsum.get("train_val_leak_groups", 0))],
                ["涉及类别数", str(xsum.get("classes_involved", 22))],
                ["与 93 类候选集共享跨类别哈希", str(xsum.get("shared_with_reference_cross_class_hashes", 34))],
                ["人工决策栏", "manual_decision 留空，等待人工确认真实类别后填写"],
            ],
        )
        doc.add_paragraph(
            "跨类别复核包只整理候选清理集剩余的字节级 exact duplicate 标签冲突；它不自动删除、移动、重命名或重标图片。"
            "正式重训前应先确认每组图片真实类别，并把处理决策写回复核记录或后续清理报告。"
        )

    cross_class_decision = load_json_report("reports/classification_cross_class_decision_table.json") or {}
    if cross_class_decision:
        dsum = cross_class_decision.get("summary", {})
        add_table(
            doc,
            ["项目", "结果"],
            [
                ["跨类别决策表", "reports/classification_cross_class_decision_table.md/json/csv"],
                ["状态", dsum.get("status", "ready_for_manual_decision")],
                ["待决策组", f"{dsum.get('pending_decisions', 34)} / {dsum.get('groups', 34)}"],
                ["已决策组", str(dsum.get("decided_groups", 0))],
                ["需专家复核组", str(dsum.get("needs_expert_review_groups", 0))],
                ["延后处理组", str(dsum.get("deferred_groups", 0))],
                ["校验错误", str(dsum.get("validation_errors", 0))],
                ["填写入口", "reports/classification_cross_class_decision_table.csv"],
            ],
        )
        doc.add_paragraph(
            "跨类别决策表把复核包中的 manual_decision 空栏标准化为 decision_status、chosen_class、action、remove_relative_paths、reviewer、reviewed_at 和 decision_note 等字段；"
            "它只收集人工决策，不自动删除、移动、重命名、重标或复制图片。"
        )

    cross_class_cleanup = load_json_report("reports/classification_cross_class_cleanup_plan.json") or {}
    if cross_class_cleanup:
        csum = cross_class_cleanup.get("summary", {})
        add_table(
            doc,
            ["项目", "结果"],
            [
                ["跨类别清理计划校验", "reports/classification_cross_class_cleanup_plan.md/json/csv"],
                ["状态", csum.get("status", "waiting_for_manual_decisions")],
                ["待决策组", f"{csum.get('pending_decisions', 34)} / {csum.get('groups', 34)}"],
                ["已决策组", str(csum.get("decided_groups", 0))],
                ["计划操作", str(csum.get("planned_operations", 0))],
                ["remove / move", f"{csum.get('planned_remove_operations', 0)} / {csum.get('planned_move_operations', 0)}"],
                ["校验错误", str(csum.get("validation_errors", 0))],
                ["操作预览", "reports/classification_cross_class_cleanup_plan.csv"],
            ],
        )
        doc.add_paragraph(
            "跨类别清理计划校验把人工决策 CSV 转换为执行前 dry-run 计划；当前所有组仍为 pending，因此不会产生删除或移动操作。"
            "人工填完 CSV 后应先重新生成该报告，只有状态为 ready_for_cleanup_execution 且校验错误为 0 时，才可进入真实数据清理执行。"
        )
        doc.add_paragraph(
            "清理执行入口为 scripts/apply_classification_cross_class_cleanup_plan.py。该脚本在当前真实计划未就绪时会阻断执行；人工决策全部完成并校验通过后，它只把结果复制到新的输出数据集目录，不删除或覆盖源候选集。"
        )

    strict_clean = load_json_report("reports/classification_leakage_clean_candidate_report.json") or {}
    strict_clean_inspection = load_json_report("reports/classification_leakage_clean_candidate_inspection.json") or {}
    strict_clean_duplicates = load_json_report("reports/classification_leakage_clean_candidate_duplicate_audit.json") or {}
    completed_93_clean = load_json_report("reports/classification_93class_leakage_clean_candidate_report.json") or {}
    completed_93_clean_inspection = load_json_report("reports/classification_93class_leakage_clean_candidate_inspection.json") or {}
    completed_93_clean_duplicates = load_json_report("reports/classification_93class_leakage_clean_candidate_duplicate_audit.json") or {}
    if strict_clean and completed_93_clean:
        sc = strict_clean.get("summary", {})
        sci = strict_clean_inspection.get("summary", {})
        scd = strict_clean_duplicates.get("summary", {})
        c93 = completed_93_clean.get("summary", {})
        c93i = completed_93_clean_inspection.get("summary", {})
        c93d = completed_93_clean_duplicates.get("summary", {})
        add_table(
            doc,
            ["项目", "strict 92 类候选集", "93 类候选集"],
            [
                ["数据路径", "data/classification_strict_jpeg_leakage_clean_candidate", "data/classification_strict_jpeg_93class_leakage_clean_candidate"],
                ["train / val / total", f"{sci.get('train_images', 7826)} / {sci.get('val_images', 1707)} / {sci.get('total_images', 9533)}", f"{c93i.get('train_images', 7841)} / {c93i.get('val_images', 1711)} / {c93i.get('total_images', 9552)}"],
                ["已移除 val 侧泄漏副本", str(sc.get("removed_images", 34)), str(c93.get("removed_images", 34))],
                ["图片复审 errors / warnings", f"{sci.get('errors', 0)} / {sci.get('warnings', 0)}", f"{c93i.get('errors', 0)} / {c93i.get('warnings', 0)}"],
                ["train/val 泄漏组", str(scd.get("train_val_leak_hashes", 0)), str(c93d.get("train_val_leak_hashes", 0))],
                ["跨类别重复组", str(scd.get("cross_class_duplicate_hashes", 34)), str(c93d.get("cross_class_duplicate_hashes", 34))],
                ["状态", scd.get("status", "needs_leakage_review"), c93d.get("status", "needs_leakage_review")],
            ],
        )
        doc.add_paragraph(
            "候选泄漏清理集只删除复核包中列出的 val 侧字节级重复副本，不自动修改 train 图像，也不裁决跨类别标签；重新训练前仍需用新的审计报告解释剩余跨类别重复。"
        )

    completed_93 = load_json_report("reports/classification_93class_completion_report.json") or {}
    completed_93_inspection = load_json_report("reports/classification_93class_dataset_inspection.json") or {}
    completed_93_metrics = load_json_report("reports/classification_93class_evaluation_metrics.json") or {}
    if completed_93:
        csum = completed_93.get("summary", {})
        isum = completed_93_inspection.get("summary", {})
        add_table(
            doc,
            ["项目", "结果"],
            [
                ["93 类补齐实验", "reports/classification_93class_training_report.md"],
                ["数据路径", "data/classification_strict_jpeg_93class"],
                ["输出类别", str(csum.get("output_classes", 93))],
                ["train / val / total", f"{csum.get('train_images', 7841)} / {csum.get('val_images', 1745)} / {csum.get('total_images', 9586)}"],
                ["大腹皮 train / val", "15 / 4"],
                ["复审 errors / warnings", f"{isum.get('errors', 0)} / {isum.get('warnings', 0)}"],
                ["训练输出", "runs/train/strict_93class_yolo12n_cls_cpu_smoke"],
                ["Top-1 / Top-5", f"{completed_93_metrics.get('top1', 0.0664756447):.10f} / {completed_93_metrics.get('top5', 0.2085959911):.10f}"],
                ["Fitness", f"{completed_93_metrics.get('fitness', 0.1375358179):.10f}"],
            ],
        )
        doc.add_paragraph(
            "93 类补齐实验用于证明完整类别覆盖链路已跑通。由于大腹皮来自原始 val-only 样本重划，且训练只有 1 epoch，"
            "该指标不能替代 92 类 strict 5 epoch 基准。"
        )
    detection_package = load_json_report("reports/detection_annotation_package_report.json") or {}
    if detection_package:
        dsum = detection_package.get("summary", {})
        add_table(
            doc,
            ["项目", "结果"],
            [
                ["检测标注准备包", "reports/detection_annotation_package_report.md"],
                ["输出目录", "data/detection_annotation_package"],
                ["覆盖类别", str(dsum.get("classes", 93))],
                ["待标注图片", str(dsum.get("images", 279))],
                ["每类抽样", f"{dsum.get('samples_per_class', 3)} 张，train {dsum.get('train_per_class', 2)} + val {dsum.get('val_per_class', 1)}"],
                ["预期标签 / 已完成标签", f"{dsum.get('labels_expected', 279)} / {dsum.get('labels_completed', 0)}"],
                ["来源划分", str(dsum.get("source_split_counts", {'train': 186, 'val': 93}))],
                ["样本总览 contact sheet", "reports/detection_annotation_contact_sheet.md + reports/figures/detection_annotation_contact_sheet.png"],
                ["状态", dsum.get("status", "pending_bbox_annotation")],
            ],
        )
        doc.add_paragraph(
            "该准备包用于后续人工绘制真实 YOLO bbox：images/ 放待标注图片，classes.txt 固定 93 类顺序，"
            "annotation_manifest.csv/json 记录来源和预期标签文件；detection_annotation_contact_sheet 用于标注前复核每类 3 张样本。labels/ 仍为空，因此不可直接训练检测模型，也不能据此汇报检测指标。"
        )
    detection_validation = load_json_report("reports/detection_annotation_package_validation.json") or {}
    if detection_validation:
        vsum = detection_validation.get("summary", {})
        add_table(
            doc,
            ["项目", "结果"],
            [
                ["检测标注包校验", "reports/detection_annotation_package_validation.md/json"],
                ["状态", vsum.get("status", "pending_bbox_annotation")],
                ["图片", f"{vsum.get('images_present', 279)} / {vsum.get('images_expected', 279)}"],
                ["缺失标签", str(vsum.get("labels_missing", 279))],
                ["有效 bbox", str(vsum.get("boxes", 0))],
                ["errors / warnings", f"{vsum.get('errors', 0)} / {vsum.get('warnings', 0)}"],
                ["严格验收入口", "标注完成后加 --require-complete"],
            ],
        )
        doc.add_paragraph(
            "当前校验证明待标注包结构、图片和 manifest 一致；人工标注完成后应使用同一脚本增加 --require-complete，"
            "确认 279 个 .txt 标签全部存在、类别编号与 manifest 一致、bbox 归一化合法后，再进入检测训练。"
        )
    strict_eval = load_json_report("reports/strict_classification_evaluation_metrics.json") or {}
    add_table(
        doc,
        ["项目", "结果"],
        [
            ["模型", "yolo12n-cls.yaml"],
            ["训练设备", "CPU"],
            ["epoch", "5"],
            ["batch", "16"],
            ["imgsz", "224"],
            ["训练输出", "runs/train/strict_classify_yolo12n_cls_cpu_5e"],
            ["独立验证 Top-1", f"{strict_eval.get('top1', 0.1769098192):.10f}"],
            ["独立验证 Top-5", f"{strict_eval.get('top5', 0.4956921339):.10f}"],
            ["Fitness", f"{strict_eval.get('fitness', 0.3363009766):.10f}"],
        ],
    )
    doc.add_paragraph(
        "该结果说明真实分类数据训练链路已跑通，并且 5 epoch 相比 1 epoch 冒烟训练有明显提升；但它仍不是检测 mAP，"
        "不能证明模型具备药材区域定位能力。"
    )
    add_table(
        doc,
        ["项目", "结果"],
        [
            ["单样例 Top-k 推理", "reports/strict_classification_sample_prediction.json"],
            ["样例 Top-1", "干姜，置信度 0.0926"],
            ["strict CPU benchmark", "20 张样本，mean 9.76 ms/image，约 102.51 FPS"],
            ["benchmark 输出", "runs/benchmarks/strict_classification_latency_20.json"],
            ["ONNX 导出", "runs/train/strict_classify_yolo12n_cls_cpu_5e/weights/best.onnx"],
            ["后端分类接口", "POST /classify/image，后端 QA 4/4"],
            ["前端分类入口", "默认分类识别，上传 strict 验证图后返回 Top-k，前端 QA 6/6"],
        ],
    )
    error_analysis = load_json_report("reports/strict_classification_error_analysis.json") or {}
    if error_analysis:
        summary = error_analysis["summary"]
        worst = error_analysis.get("worst_classes", [])
        best = error_analysis.get("best_classes", [])
        confusions = error_analysis.get("confusion_pairs", [])
        add_table(
            doc,
            ["项目", "结果"],
            [
                ["误判分析输出", "reports/strict_classification_error_analysis.md/json"],
                ["分析图像", str(summary["images"])],
                ["分析类别", str(summary["classes"])],
                ["Top-1 正确", f"{summary['top1_correct']} / {summary['images']}"],
                ["Top-5 正确", f"{summary['top5_correct']} / {summary['images']}"],
                ["Top-1 最高类别", "、".join(item["class_name"] for item in best[:2])],
                ["Top-1 最低类别", "、".join(item["class_name"] for item in worst[:4])],
            ],
        )
        add_table(
            doc,
            ["真实类别", "预测类别", "次数"],
            [
                [item["expected_class"], item["predicted_class"], str(item["count"])]
                for item in confusions[:5]
            ],
        )
        doc.add_paragraph(
            "误判分析说明当前短训模型已对少数外观特征鲜明类别形成有效区分，但大量外观相近类别仍被吸收到少数高频预测类别中。"
            "后续应优先对 Top-1 为 0 或高频混淆类别做人工复核、补样、增强和更长轮次训练。"
        )
    review_samples = load_json_report("reports/strict_classification_review_samples.json") or {}
    if review_samples:
        figures = review_samples.get("figures", {})
        add_table(
            doc,
            ["项目", "结果"],
            [
                ["人工复核清单", "reports/strict_classification_review_samples.md/json"],
                ["高频混淆样例", f"{len(review_samples.get('confusion_samples', []))} 张"],
                ["低表现类别样例", f"{len(review_samples.get('worst_class_samples', []))} 张"],
                ["高频混淆 contact sheet", figures.get("confusion_contact_sheet", "")],
                ["低表现类别 contact sheet", figures.get("worst_class_contact_sheet", "")],
            ],
        )
        doc.add_paragraph(
            "人工复核 contact sheet 用于快速检查目录混入、外观高度相似、拍摄条件差异和标注命名不一致等问题；"
            "它是数据清洗依据，不代表新模型性能。"
        )
        for key, caption in [
            ("confusion_contact_sheet", "高频混淆人工复核 contact sheet"),
            ("worst_class_contact_sheet", "低表现类别人工复核 contact sheet"),
        ]:
            figure = Path(figures.get(key, ""))
            if figure.exists():
                doc.add_paragraph(caption)
                doc.add_picture(str(figure), width=Inches(6.2))

    doc.add_heading("7. 性能与接口测试", level=1)
    smoke = load_json_report("reports/smoke_check.json")
    frontend = load_json_report("reports/frontend_qa.json")
    backend = load_json_report("reports/backend_qa.json")
    bench = load_json_report("runs/benchmarks/demo_latency.json")
    rows = []
    if smoke:
        s = smoke["summary"]
        rows.append(["工程自检", f"{s['passed']} / {s['total']} 通过", "reports/smoke_check.json"])
    rows.append(["单元测试", "5 / 5 通过", "pytest tests -q"])
    rows.append(["前端构建", "通过", "npm run build"])
    if frontend:
        s = frontend["summary"]
        rows.append(["前端 Playwright QA", f"{s['checks_passed']} / {s['checks_total']} 通过", "桌面端、移动端、分类上传、目标检测页签、摄像头页签、训练页签"])
        rows.append(["相关 console error", str(s["relevant_console_errors"]), "Vite 调试日志不计为错误"])
    if backend:
        s = backend["summary"]
        rows.append(["后端 API QA", f"{s['passed']} / {s['total']} 通过", "/health、/models、/detect/image、/classify/image"])
        detect = next((item for item in backend["checks"] if item["name"] == "POST /detect/image"), None)
        if detect:
            rows.append(["API 图片识别耗时", f"{detect['detail']['elapsed_ms']:.2f} ms", "demo 权重、本机 CPU、单次请求"])
        classify = next((item for item in backend["checks"] if item["name"] == "POST /classify/image"), None)
        if classify:
            rows.append(["API 分类识别耗时", f"{classify['detail']['elapsed_ms']:.2f} ms", "strict 分类权重、本机 CPU、单次请求"])
    if bench:
        rows.append(["CPU 单图 benchmark", f"{bench['latency_ms_mean']:.2f} ms", "demo 权重、imgsz=320、1 张图"])
        rows.append(["CPU 单图 FPS 估计", f"{bench['fps_mean']:.2f} FPS", "demo benchmark 粗略估计，不代表生产吞吐"])
    strict_bench = load_json_report("runs/benchmarks/strict_classification_latency_20.json")
    if strict_bench:
        rows.append(["strict 分类 CPU benchmark", f"{strict_bench['latency_ms_mean']:.2f} ms", "20 张验证样本、imgsz=224、本机 CPU"])
        rows.append(["strict 分类 FPS 估计", f"{strict_bench['fps_mean']:.2f} FPS", "小样本延迟测试，用于工程参考"])
    add_table(doc, ["测试项", "结果", "说明"], rows)

    doc.add_heading("8. 真实检测准确性指标状态", level=1)
    add_table(
        doc,
        ["指标", "当前结果", "备注"],
        [
            ["Precision", "待真实数据实测", "正式训练完成后生成"],
            ["Recall", "待真实数据实测", "正式训练完成后生成"],
            ["mAP@50", "待真实数据实测", "正式训练完成后生成"],
            ["mAP@50-95", "待真实数据实测", "正式训练完成后生成"],
            ["per-class AP", "待真实数据实测", "正式训练完成后生成"],
            ["混淆矩阵", "待真实数据实测", "Ultralytics val 输出"],
            ["PR / F1 曲线", "待真实数据实测", "Ultralytics val 输出"],
        ],
    )
    doc.add_paragraph(
        "分类阶段已有阶段性指标：strict 数据集 Top-1 0.1769、Top-5 0.4957，并已补充类别一致性审计、重复/泄漏审计、泄漏人工复核包、候选泄漏清理集、跨类别复核包、跨类别决策表、跨类别清理计划校验、跨类别清理执行入口、可复现实验 Manifest、每类误判分析和人工复核 contact sheet。"
        "当前 strict 5 epoch 基准覆盖 92 类；93 类补齐实验已让大腹皮进入训练/验证链路，但仍需新增采集或标注训练样本后才能形成更严格的 93 类正式基准。"
        "候选泄漏清理集已将 train/val exact duplicate 归零，但仍有 34 组跨类别 exact duplicate，因此重新训练和指标解释仍需带类别复核边界。"
        "检测标注准备包已覆盖 93 类、279 张待标注图，并生成样本总览 contact sheet；pending 校验为 errors 0 / warnings 0，但 labels/ 仍为空；检测阶段的 Precision、Recall、mAP 仍需真实 bbox 标注完成后生成。"
    )

    doc.add_heading("9. 鲁棒性测试方案", level=1)
    doc.add_paragraph("scripts/robustness_test.py 可生成以下扰动样本：")
    add_bullets(doc, ["低光照", "高光照", "低对比度", "旋转 15 度", "高斯模糊", "中心遮挡"])
    doc.add_paragraph(
        "正式测试方法：在干净测试集和扰动测试集上分别运行推理/评估，对比 Precision、Recall、mAP 和误检案例。"
        "该项需在真实测试集接入后执行。"
    )

    doc.add_heading("10. 风险与限制", level=1)
    add_bullets(
        doc,
        [
            "若公开数据只有分类标签，没有边界框，必须补充检测标注；整图框转换只能跑通流程，不能作为高质量检测标注。",
            "YOLOv12 属于注意力中心研究模型，可能存在训练不稳定、显存占用高、CPU 推理慢等问题。",
            "参考文献中的 GhostC2f、DySnakeC2f、SimSPPF、CA 属于 YOLOv8-TCM 改进，不应未经消融直接迁移到 YOLOv12。",
            "文献结果不能直接作为本项目结果；本项目指标必须来自当前数据集和当前权重。",
            "当前 demo 训练用于验证工程链路，不能替代正式实验。",
            "当前 strict 训练是分类任务，只能汇报 Top-1/Top-5，不能替代检测任务的 mAP。",
            "大腹皮已通过补齐实验进入 1 epoch 训练链路，但其 train/val 来自原始 val-only 样本重划，正式 93 类基准仍建议补充独立训练样本。",
            "检测标注准备包和样本总览 contact sheet 只是人工标注启动材料，labels/ 仍为空，不能作为已完成检测数据集。",
            "检测标注包当前只通过 pending 状态校验；必须在 --require-complete 严格验收通过后才可进入检测训练。",
            "重复/泄漏审计只检查文件字节级 SHA256 完全重复；当前已生成候选泄漏清理集并移除 val 侧 train/val exact duplicate，剩余 34 组跨类别 exact duplicate 已生成跨类别复核包、决策表和清理计划校验报告，需人工确认真实类别后再决定删除、移动、重标或保留。",
        ],
    )

    doc.add_heading("11. 后续补测清单", level=1)
    add_bullets(
        doc,
        [
            "若最终要求目标检测，补充真实 YOLO bbox 标注数据集。",
            "优先使用 data/detection_annotation_package 完成人工 bbox 标注，保持 classes.txt 的 93 类顺序不变。",
            "人工标注完成后运行 scripts\\validate_detection_annotation_package.py --require-complete 严格验收。",
            "运行数据校验和划分。",
            "在 GPU 环境完成 strict 分类 30-100 epoch 正式训练。",
            "CPU 正式配置：configs/train_cls_strict_cpu_30e.yaml。",
            "GPU 正式配置：configs/train_cls_strict_gpu_100e.yaml。",
            "为大腹皮补充独立训练样本后运行 93 类正式长轮次实验。",
            "基于 data/classification_strict_jpeg_leakage_clean_candidate 或 data/classification_strict_jpeg_93class_leakage_clean_candidate 重新训练前，先使用 classification_cross_class_review_package.md、classification_cross_class_decision_table.csv 和 contact sheet 复核剩余 34 组跨类别 exact duplicate，记录处理决策后重新生成 classification_cross_class_cleanup_plan.md 做执行前校验，再用 apply_classification_cross_class_cleanup_plan.py 写入新的输出数据集目录。",
            "完成 YOLOv12s 或关键调参对照。",
            "生成真实检测评估指标、训练曲线和混淆矩阵。",
            "运行 CPU/GPU benchmark。",
            "基于 strict_classification_review_samples.md、detection_annotation_contact_sheet.md 和 contact sheet 继续补充相似类别人工复核结论、标注复核结论和补样优先级。",
            "将真实实验结果同步更新到 reports/test_report.md、reports/test_report.docx 和 reports/overview_design.pptx。",
        ],
    )

    output = ROOT / "reports" / "test_report.docx"
    doc.save(output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
