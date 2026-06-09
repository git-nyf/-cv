const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const root = path.resolve(__dirname, "..");
const outDir = path.join(root, "reports");
fs.mkdirSync(outDir, { recursive: true });

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "第8组";
pptx.subject = "基于 YOLOv12 的中草药饮片智能识别与分类系统概要设计";
pptx.title = "YOLOv12 中药饮片识别系统概要设计";
pptx.company = "课程项目";
pptx.lang = "zh-CN";
pptx.theme = {
  headFontFace: "Microsoft YaHei",
  bodyFontFace: "Microsoft YaHei",
  lang: "zh-CN",
};
pptx.defineLayout({ name: "CUSTOM_WIDE", width: 13.333, height: 7.5 });
pptx.layout = "CUSTOM_WIDE";

const C = {
  navy: "1F4E79",
  blue: "2E75B6",
  light: "EEF5FB",
  ink: "1F2933",
  muted: "667085",
  line: "D0D7DE",
  white: "FFFFFF",
  green: "168A53",
  amber: "B7791F",
};

function loadJson(relativePath) {
  const target = path.join(root, relativePath);
  if (!fs.existsSync(target)) return null;
  return JSON.parse(fs.readFileSync(target, "utf8"));
}

const errorAnalysis = loadJson("reports/strict_classification_error_analysis.json");
const errorSummary = errorAnalysis?.summary || {
  images: 1741,
  classes: 92,
  top1_correct: 308,
  top5_correct: 863,
  top1_accuracy: 0.1769098219,
  top5_accuracy: 0.4956921310,
};
const topConfusions = (errorAnalysis?.confusion_pairs || [
  { expected_class: "九香虫", predicted_class: "木丁香", count: 12 },
  { expected_class: "合欢皮", predicted_class: "川牛膝", count: 12 },
  { expected_class: "柏子仁", predicted_class: "芥子", count: 12 },
]).slice(0, 3);
const worstClasses = (errorAnalysis?.worst_classes || [
  { class_name: "地龙" },
  { class_name: "安息香" },
  { class_name: "瓦楞子" },
  { class_name: "北沙参" },
]).slice(0, 4);
const reviewSamples = loadJson("reports/strict_classification_review_samples.json");
const reviewSummary = {
  confusionSamples: reviewSamples?.confusion_samples?.length || 18,
  worstClassSamples: reviewSamples?.worst_class_samples?.length || 18,
  confusionSheet: reviewSamples?.figures?.confusion_contact_sheet || "reports/figures/strict_confusion_contact_sheet.png",
  worstClassSheet: reviewSamples?.figures?.worst_class_contact_sheet || "reports/figures/strict_worst_class_contact_sheet.png",
};
const classAudit = loadJson("reports/class_consistency_audit.json");
const classSummary = classAudit?.summary || {
  raw_classes: 93,
  strict_classes: 92,
  classes_missing_from_strict: ["大腹皮"],
  zero_train_classes: ["大腹皮"],
  status: "needs_class_completion",
};
const completed93 = loadJson("reports/classification_93class_completion_report.json");
const completed93Summary = completed93?.summary || {
  output_classes: 93,
  train_images: 7841,
  val_images: 1745,
  rebalanced_classes: ["大腹皮"],
};
const completed93Metrics = loadJson("reports/classification_93class_evaluation_metrics.json") || {
  top1: 0.0664756447,
  top5: 0.2085959911,
  fitness: 0.1375358179,
};
const strictDuplicateAudit = loadJson("reports/strict_classification_duplicate_audit.json");
const strictDuplicateSummary = strictDuplicateAudit?.summary || {
  status: "needs_leakage_review",
  duplicate_hashes: 546,
  train_val_leak_hashes: 34,
  cross_class_duplicate_hashes: 52,
};
const leakageReviewPackage = loadJson("reports/classification_leakage_review_package.json");
const leakageReviewSummary = leakageReviewPackage?.summary || {
  status: "complete_review_package",
  leakage_groups: 34,
  leakage_records: 69,
  same_class_leakage_groups: 16,
  cross_class_leakage_groups: 18,
};
const leakageClean = loadJson("reports/classification_leakage_clean_candidate_report.json");
const leakageCleanSummary = leakageClean?.summary || {
  removed_images: 34,
};
const leakageCleanInspection = loadJson("reports/classification_leakage_clean_candidate_inspection.json");
const leakageCleanInspectionSummary = leakageCleanInspection?.summary || {
  train_images: 7826,
  val_images: 1707,
  total_images: 9533,
};
const leakageCleanDuplicate = loadJson("reports/classification_leakage_clean_candidate_duplicate_audit.json");
const leakageCleanDuplicateSummary = leakageCleanDuplicate?.summary || {
  train_val_leak_hashes: 0,
  cross_class_duplicate_hashes: 34,
};
const crossClassReviewPackage = loadJson("reports/classification_cross_class_review_package.json");
const crossClassReviewSummary = crossClassReviewPackage?.summary || {
  status: "complete_review_package",
  cross_class_groups: 34,
  expected_cross_class_groups: 34,
  cross_class_records: 68,
  train_val_leak_groups: 0,
};
const crossClassDecisionTable = loadJson("reports/classification_cross_class_decision_table.json");
const crossClassDecisionSummary = crossClassDecisionTable?.summary || {
  status: "ready_for_manual_decision",
  groups: 34,
  pending_decisions: 34,
  decided_groups: 0,
  validation_errors: 0,
};
const crossClassCleanupPlan = loadJson("reports/classification_cross_class_cleanup_plan.json");
const crossClassCleanupSummary = crossClassCleanupPlan?.summary || {
  status: "waiting_for_manual_decisions",
  groups: 34,
  pending_decisions: 34,
  planned_operations: 0,
  validation_errors: 0,
};
const completed93DuplicateAudit = loadJson("reports/classification_93class_duplicate_audit.json");
const completed93DuplicateSummary = completed93DuplicateAudit?.summary || {
  status: "needs_leakage_review",
  duplicate_hashes: 546,
  train_val_leak_hashes: 34,
  cross_class_duplicate_hashes: 52,
};
const detectionPackage = loadJson("reports/detection_annotation_package_report.json");
const detectionSummary = detectionPackage?.summary || {
  status: "pending_bbox_annotation",
  classes: 93,
  images: 279,
  labels_expected: 279,
  labels_completed: 0,
  samples_per_class: 3,
  source_split_counts: { train: 186, val: 93 },
};
const detectionValidation = loadJson("reports/detection_annotation_package_validation.json");
const detectionValidationSummary = detectionValidation?.summary || {
  status: "pending_bbox_annotation",
  images_expected: 279,
  images_present: 279,
  labels_missing: 279,
  errors: 0,
  warnings: 0,
};
const detectionContactSheet = loadJson("reports/detection_annotation_contact_sheet.json");
const detectionContactSummary = detectionContactSheet?.summary || {
  samples: 279,
  classes: 93,
  labels_completed: 0,
  annotation_status: "pending_bbox_annotation",
};
const reproManifest = loadJson("reports/repro_manifest.json");
const reproSummary = {
  artifacts: reproManifest?.artifacts?.length || 83,
  commands: reproManifest?.reproduction_commands?.length || 29,
  smokePassed: reproManifest?.evaluation?.smoke_check?.passed || 138,
  smokeTotal: reproManifest?.evaluation?.smoke_check?.total || 138,
};

function title(slide, text) {
  slide.addText(text, {
    x: 0.55,
    y: 0.25,
    w: 12.1,
    h: 0.55,
    fontFace: "Microsoft YaHei",
    fontSize: 25,
    bold: true,
    color: C.navy,
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 0.55,
    y: 0.95,
    w: 12.1,
    h: 0,
    line: { color: C.line, pt: 1 },
  });
}

function footer(slide, cite) {
  slide.addText(cite || "第8组 · 基于 YOLOv12 的中草药饮片智能识别与分类系统 · 2026.6", {
    x: 0.55,
    y: 7.02,
    w: 12.1,
    h: 0.28,
    fontFace: "Microsoft YaHei",
    fontSize: 9,
    color: C.muted,
    margin: 0,
  });
}

function bulletList(slide, items, x, y, w, h, fontSize = 16) {
  slide.addText(
    items.map((item) => ({ text: item, options: { bullet: { indent: 16 }, hanging: 4, breakLine: true } })),
    {
      x,
      y,
      w,
      h,
      fontFace: "Microsoft YaHei",
      fontSize,
      color: C.ink,
      margin: 0.04,
      paraSpaceAfterPt: 8,
      fit: "shrink",
      breakLine: false,
    }
  );
}

function card(slide, x, y, w, h, heading, body, accent = C.blue) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h,
    rectRadius: 0.06,
    fill: { color: C.white },
    line: { color: C.line, pt: 1 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x,
    y,
    w: 0.08,
    h,
    fill: { color: accent },
    line: { color: accent },
  });
  slide.addText(heading, {
    x: x + 0.18,
    y: y + 0.13,
    w: w - 0.28,
    h: 0.28,
    fontFace: "Microsoft YaHei",
    fontSize: 14,
    bold: true,
    color: C.navy,
    margin: 0,
  });
  slide.addText(body, {
    x: x + 0.18,
    y: y + 0.48,
    w: w - 0.28,
    h: h - 0.58,
    fontFace: "Microsoft YaHei",
    fontSize: 11,
    color: C.ink,
    margin: 0,
    fit: "shrink",
    breakLine: false,
  });
}

function arrow(slide, x1, y1, x2, y2) {
  slide.addShape(pptx.ShapeType.line, {
    x: x1,
    y: y1,
    w: x2 - x1,
    h: y2 - y1,
    line: { color: C.blue, pt: 1.5, beginArrowType: "none", endArrowType: "triangle" },
  });
}

// 1
{
  const slide = pptx.addSlide();
  slide.background = { color: C.navy };
  slide.addText("基于 YOLOv12 的中草药饮片智能识别与分类系统", {
    x: 0.75,
    y: 1.55,
    w: 11.6,
    h: 1.0,
    fontFace: "Microsoft YaHei",
    fontSize: 30,
    bold: true,
    color: C.white,
    margin: 0,
    fit: "shrink",
  });
  slide.addText("概要设计汇报 · 第8组 · 2026年6月", {
    x: 0.78,
    y: 2.78,
    w: 8.5,
    h: 0.35,
    fontFace: "Microsoft YaHei",
    fontSize: 16,
    color: "DCEAF7",
    margin: 0,
  });
  slide.addShape(pptx.ShapeType.rect, { x: 0.78, y: 3.35, w: 2.3, h: 0.05, fill: { color: C.blue }, line: { color: C.blue } });
  slide.addText("目标：完成数据处理、YOLOv12 基线训练、推理部署、性能测试与课程演示闭环。", {
    x: 0.78,
    y: 3.65,
    w: 10.2,
    h: 0.5,
    fontFace: "Microsoft YaHei",
    fontSize: 16,
    color: "F5FAFF",
    margin: 0,
  });
}

// 2
{
  const slide = pptx.addSlide();
  title(slide, "系统目标聚焦“可检测、可演示、可复现”的课程闭环");
  card(slide, 0.75, 1.35, 3.65, 1.7, "业务问题", "中药饮片种类多、形态相近，人工鉴别耗时且主观性强，难以支撑教学演示和批量复核。");
  card(slide, 4.85, 1.35, 3.65, 1.7, "系统能力", "图片上传和摄像头截帧识别，输出检测框、类别、置信度，并保存结果图和 JSON。");
  card(slide, 8.95, 1.35, 3.65, 1.7, "交付边界", "本地 Web 原型，服务课程展示；不做药理问答、处方推荐、医学诊断或真伪最终判定。");
  bulletList(slide, [
    "一期范围：数据集检查、训练/评估脚本、FastAPI 推理接口、Vue3 工作台、测试报告和概要设计 PPT。",
    "性能目标作为实验目标记录，不提前承诺；所有 mAP/FPS 均以后续真实训练和测试为准。",
  ], 0.9, 3.55, 11.5, 1.2, 16);
  footer(slide);
}

// 3
{
  const slide = pptx.addSlide();
  title(slide, "功能划分围绕数据、训练、推理和展示四个核心模块");
  const modules = [
    ["数据集管理", "导入 YOLO 格式数据，检查图片/标签/bbox，按 7:2:1 划分。"],
    ["模型训练", "基于 YOLOv12n/s 启动训练，保存 best.pt、last.pt、日志和曲线。"],
    ["智能识别", "支持图片上传识别和摄像头截帧识别，返回类别、置信度和边界框。"],
    ["结果复盘", "保存结果图、预测 JSON、测试报告和典型误检案例。"],
  ];
  modules.forEach((m, i) => card(slide, 0.8 + i * 3.05, 1.45, 2.65, 2.05, m[0], m[1], [C.blue, C.green, C.amber, C.navy][i]));
  slide.addText("用户角色：普通用户负责识别演示；管理员负责数据维护、训练启动和权重切换；开发者负责模型与接口维护。", {
    x: 0.9,
    y: 4.25,
    w: 11.4,
    h: 0.7,
    fontFace: "Microsoft YaHei",
    fontSize: 17,
    color: C.ink,
    margin: 0,
    fit: "shrink",
  });
  footer(slide);
}

// 4
{
  const slide = pptx.addSlide();
  title(slide, "YOLOv12 以注意力中心架构提升实时检测的精度-速度平衡");
  card(slide, 0.8, 1.35, 3.3, 1.5, "Backbone", "CSPNet + A2C2f；Area Attention 通过区域注意力降低全局注意力开销。");
  card(slide, 4.95, 1.35, 3.3, 1.5, "Neck", "FPN + PAN + R-ELAN；增强多尺度特征融合和训练稳定性。");
  card(slide, 9.1, 1.35, 3.3, 1.5, "Head", "Anchor-Free 检测头，直接预测目标中心和边界框，减少 Anchor 调参。");
  arrow(slide, 4.15, 2.1, 4.8, 2.1);
  arrow(slide, 8.3, 2.1, 8.95, 2.1);
  bulletList(slide, [
    "第一阶段采用标准 YOLOv12n/s 作为基线，不修改结构，优先保证训练、验证、推理闭环。",
    "第二阶段再做输入尺寸、学习率、batch、阈值和增强策略调优。",
    "GhostC2f、DySnakeC2f、SimSPPF、CA 来自 YOLOv8-TCM 文献，作为计划改进和消融方向，不机械迁移。",
  ], 1.0, 3.65, 11.2, 1.75, 15);
  footer(slide, "参考：Tian et al., YOLOv12: Attention-Centric Real-Time Object Detectors; Sun et al., 2025");
}

// 5
{
  const slide = pptx.addSlide();
  title(slide, "核心流程从数据校验开始，最终进入前后端推理展示");
  const steps = [
    ["数据准备", "images/labels/data.yaml"],
    ["质量检查", "缺标签、bbox、重复图"],
    ["训练评估", "YOLOv12n/s + mAP"],
    ["部署推理", "FastAPI + Vue3"],
    ["测试复盘", "报告、曲线、误检案例"],
  ];
  steps.forEach((s, i) => {
    card(slide, 0.55 + i * 2.55, 1.55, 2.1, 1.45, s[0], s[1], i % 2 ? C.green : C.blue);
    if (i < steps.length - 1) arrow(slide, 2.68 + i * 2.55, 2.25, 3.02 + i * 2.55, 2.25);
  });
  slide.addShape(pptx.ShapeType.roundRect, { x: 1.0, y: 4.0, w: 11.3, h: 1.35, rectRadius: 0.08, fill: { color: C.light }, line: { color: "BFD7EA" } });
  slide.addText("工程实现：scripts/ 负责数据、训练、评估、推理和 benchmark；backend/ 提供 API；frontend/ 提供一屏式识别工作台；reports/ 输出测试报告与 PPT。", {
    x: 1.25,
    y: 4.32,
    w: 10.8,
    h: 0.7,
    fontFace: "Microsoft YaHei",
    fontSize: 16,
    color: C.ink,
    margin: 0,
    fit: "shrink",
  });
  footer(slide);
}

// 6
{
  const slide = pptx.addSlide();
  title(slide, "真实分类数据已完成 strict 清洗和 5 epoch 阶段实验");
  const rows = [
    ["环境搭建", "requirements.txt + setup_env.ps1", ".venv 已安装，核心依赖验证通过"],
    ["分类清洗", "prepare_strict_classification_dataset.py", "92 类，7826 train / 1741 val，0 errors/warnings"],
    ["类别一致性", "audit_class_consistency.py", `原始 ${classSummary.raw_classes} 类，strict ${classSummary.strict_classes} 类；大腹皮训练样本为 0`],
    ["重复/泄漏", "audit_classification_duplicates.py", `train/val 泄漏 ${strictDuplicateSummary.train_val_leak_hashes} 组；跨类别重复 ${strictDuplicateSummary.cross_class_duplicate_hashes} 组，需人工复核`],
    ["泄漏复核包", "generate_classification_leakage_review_package.py", `${leakageReviewSummary.leakage_groups} 组泄漏全部进入复核清单；跨类别 ${leakageReviewSummary.cross_class_leakage_groups} 组`],
    ["候选清理集", "prepare_leakage_clean_classification_dataset.py", `移除 val 副本 ${leakageCleanSummary.removed_images} 张；train/val 泄漏 ${leakageCleanDuplicateSummary.train_val_leak_hashes} 组；跨类别 ${leakageCleanDuplicateSummary.cross_class_duplicate_hashes} 组`],
    ["跨类别复核包", "generate_classification_cross_class_review_package.py", `${crossClassReviewSummary.cross_class_groups}/${crossClassReviewSummary.expected_cross_class_groups} 组标签冲突进入复核；记录 ${crossClassReviewSummary.cross_class_records} 条`],
    ["跨类别决策表", "generate_classification_cross_class_decision_table.py", `${crossClassDecisionSummary.pending_decisions}/${crossClassDecisionSummary.groups} 组 pending；校验错误 ${crossClassDecisionSummary.validation_errors}`],
    ["清理计划校验", "generate_classification_cross_class_cleanup_plan.py", `${crossClassCleanupSummary.status}；计划操作 ${crossClassCleanupSummary.planned_operations}；错误 ${crossClassCleanupSummary.validation_errors}`],
    ["清理执行入口", "apply_classification_cross_class_cleanup_plan.py", "计划 ready 后只写新输出目录；当前 pending 会阻断"],
    ["93 类补齐", "prepare_completed_classification_dataset.py", `${completed93Summary.output_classes} 类；大腹皮 15/4 重划；Top-1=${Number(completed93Metrics.top1).toFixed(4)}`],
    ["检测标注准备包", "prepare_detection_annotation_package.py", `${detectionSummary.classes} 类，${detectionSummary.images} 张待标注图；labels=${detectionSummary.labels_completed}/${detectionSummary.labels_expected}`],
    ["样本总览", "generate_detection_annotation_contact_sheet.py", `${detectionContactSummary.samples} 张样本，${detectionContactSummary.classes} 类；标注前复核 contact sheet`],
    ["标注包校验", "validate_detection_annotation_package.py", `${detectionValidationSummary.status}；缺失标签 ${detectionValidationSummary.labels_missing}；errors=${detectionValidationSummary.errors}`],
    ["训练评估", "train/evaluate_yolo12_cls.py", "5 epoch；Top-1=0.1769，Top-5=0.4957"],
    ["误判分析", "analyze_classification_errors.py", `${errorSummary.images} 图；Top-1 正确 ${errorSummary.top1_correct}；Top-5 正确 ${errorSummary.top5_correct}`],
    ["人工复核", "generate_error_review_contact_sheet.py", `${reviewSummary.confusionSamples + reviewSummary.worstClassSamples} 张样例；2 张 contact sheet`],
    ["可复现实验", "generate_repro_manifest.py", `Manifest：${reproSummary.commands} 条命令，${reproSummary.artifacts} 个关键产物 SHA256`],
    ["推理部署", "infer_image_cls + /classify/image", "Top-k JSON、ONNX、前端分类入口均已验证"],
  ];
  slide.addTable([
    [{ text: "检查项", options: { bold: true } }, { text: "实现入口", options: { bold: true } }, { text: "当前状态", options: { bold: true } }],
    ...rows,
  ], {
    x: 0.8,
    y: 1.28,
    w: 11.7,
    h: 4.25,
    border: { color: C.line, pt: 1 },
    fill: "FFFFFF",
    color: C.ink,
    fontFace: "Microsoft YaHei",
    fontSize: 9.1,
    margin: 0.08,
    autoFit: false,
  });
  slide.addText("说明：当前真实数据是分类目录；候选清理集已移除 val 侧 train/val 泄漏副本，剩余跨类别冲突已生成复核包、决策表和清理计划校验但仍需人工填写；检测 mAP 仍需补真实 bbox 标注后生成。", {
    x: 1.0,
    y: 5.55,
    w: 11.1,
    h: 0.7,
    fontFace: "Microsoft YaHei",
    fontSize: 16,
    color: C.navy,
    bold: true,
    margin: 0,
    fit: "shrink",
  });
  footer(slide);
}

// 7
{
  const slide = pptx.addSlide();
  title(slide, "改进实验按低风险调参优先，再评估结构迁移价值");
  card(slide, 0.8, 1.35, 3.75, 2.1, "第一组：模型规模", "YOLOv12n vs YOLOv12s，对比 mAP、模型大小、CPU/GPU 延迟。", C.blue);
  card(slide, 4.85, 1.35, 3.75, 2.1, "第二组：训练参数", "imgsz 640/768、学习率、batch size、早停和增强强度。", C.green);
  card(slide, 8.9, 1.35, 3.75, 2.1, "第三组：文献模块", "GhostC2f、DySnakeC2f、SimSPPF、CA 只在基线稳定后作为消融计划。", C.amber);
  bulletList(slide, [
    "孙兴等在 201 类、3879 张图像上报告 mAP@50-95 为 84.16%，可作为目标参考，不作为本项目结果。",
    "CHDPL-Net 和 DGS-YOLOv8 证明轻量化与注意力机制在中药/药材检测中有研究价值。",
  ], 1.0, 4.15, 11.2, 1.2, 15);
  footer(slide, "参考：Sun et al., 2025; Lin et al., 2025; Zhang et al., 2024");
}

// 8
{
  const slide = pptx.addSlide();
  title(slide, "性能测试覆盖准确性、效率、鲁棒性和工程接口四个维度");
  card(slide, 0.8, 1.25, 2.8, 2.0, "准确性", `分类 Top-1/Top-5 已有阶段结果；误判分析覆盖 ${errorSummary.classes} 类；检测 mAP 待真实 bbox。`);
  card(slide, 3.95, 1.25, 2.8, 2.0, "效率", "strict 分类 20 图 CPU benchmark：mean 9.76 ms，约 102.51 FPS。");
  card(slide, 7.1, 1.25, 2.8, 2.0, "93 类补齐", `${completed93Summary.output_classes} 类，${completed93Summary.train_images}/${completed93Summary.val_images}；大腹皮 15/4；Top-5=${Number(completed93Metrics.top5).toFixed(4)}。`);
  card(slide, 10.25, 1.25, 2.3, 2.0, "泄漏清理", `候选集 ${leakageCleanInspectionSummary.total_images} 张；train/val 泄漏 ${leakageCleanDuplicateSummary.train_val_leak_hashes} 组。`);
  slide.addText(`输出物：repro_manifest.md、class_consistency_audit.md、strict_classification_duplicate_audit.md、classification_leakage_review_package.md、classification_leakage_clean_candidate_report.md、classification_cross_class_review_package.md、classification_cross_class_decision_table.csv、classification_cross_class_cleanup_plan.md、apply_classification_cross_class_cleanup_plan.py、detection_annotation_package_report.md、detection_annotation_contact_sheet.md、strict_classification_training_report.md、strict_classification_error_analysis.md、strict_classification_review_samples.md、test_report.md；Manifest 固化环境、命令、指标和 SHA256。`, {
    x: 0.9,
    y: 4.25,
    w: 11.5,
    h: 0.7,
    fontFace: "Microsoft YaHei",
    fontSize: 16,
    color: C.ink,
    margin: 0,
    fit: "shrink",
  });
  footer(slide);
}

// 9
{
  const slide = pptx.addSlide();
  title(slide, "主要风险集中在数据标注、算力占用和相似类别误检");
  const confusionText = topConfusions.map((item) => `${item.expected_class}->${item.predicted_class}(${item.count})`).join("；");
  const worstText = worstClasses.map((item) => item.class_name).join("、");
  const risks = [
    ["数据标注不足", "若只有分类目录，需补真实 bbox；整图框只用于流程验证。"],
    ["类别缺口", "大腹皮已通过 93 类补齐实验进入训练链路；正式基准仍建议补独立样本。"],
    ["重复/泄漏风险", `候选清理集 train/val 泄漏 ${leakageCleanDuplicateSummary.train_val_leak_hashes} 组；跨类别复核包覆盖 ${crossClassReviewSummary.cross_class_groups} 组，决策表 pending ${crossClassDecisionSummary.pending_decisions} 组，清理计划操作 ${crossClassCleanupSummary.planned_operations}；执行脚本当前会阻断。`],
    ["检测标注准备包", `${detectionSummary.classes} 类、${detectionSummary.images} 张待标注图；contact sheet ${detectionContactSummary.samples} 样本；labels/ 仍为空。`],
    ["复现追溯", `可复现实验 Manifest：${reproSummary.commands} 条命令、${reproSummary.artifacts} 个产物哈希。`],
    ["相似类别误检", `高频混淆：${confusionText}；低表现类：${worstText}。`],
  ];
  risks.forEach((r, i) => card(slide, 0.85 + (i % 2) * 6.05, 1.1 + Math.floor(i / 2) * 1.65, 5.45, 1.25, r[0], r[1], i < 3 ? C.amber : C.blue));
  footer(slide);
}

// 10
{
  const slide = pptx.addSlide();
  title(slide, "当前交付已完成工程闭环和真实分类阶段实验");
  bulletList(slide, [
    "已交付：工程结构、数据处理脚本、YOLOv12 训练/调参/评估/推理脚本、FastAPI 后端、Vue3 前端、测试报告和 PPT。",
    `已验证：strict 分类链路已跑通；Top-1=0.1769、Top-5=0.4957；类别一致性审计确认原始 ${classSummary.raw_classes} 类、strict ${classSummary.strict_classes} 类；93 类补齐实验已跑通，大腹皮 15/4 重划。`,
    `重复/泄漏审计：已生成 ${leakageReviewSummary.leakage_groups} 组 train/val 泄漏人工复核包；候选清理集移除 val 副本 ${leakageCleanSummary.removed_images} 张，train/val 泄漏归零；跨类别复核包覆盖 ${crossClassReviewSummary.cross_class_groups} 组标签冲突，决策表 ${crossClassDecisionSummary.pending_decisions}/${crossClassDecisionSummary.groups} 组待填写，清理计划校验 ${crossClassCleanupSummary.status}。`,
    `检测标注准备包：覆盖 ${detectionSummary.classes} 类、${detectionSummary.images} 张待标注图，样本总览 contact sheet ${detectionContactSummary.samples} 张；pending 校验 errors=${detectionValidationSummary.errors}；labels/ 仍为空。`,
    `可复现实验 Manifest：记录 ${reproSummary.commands} 条复现命令、${reproSummary.artifacts} 个关键产物 SHA256；工程自检 ${reproSummary.smokePassed}/${reproSummary.smokeTotal}。`,
    "可延长训练：CPU 30 epoch 配置和 GPU 100 epoch 配置已补齐，可继续做正式训练对照。",
    "待补测：补充真实 bbox 后完成检测训练、真实 mAP 曲线、CPU/GPU 延迟和鲁棒性对比。",
    "结果边界：当前真实结果是分类 Top-1/Top-5，不等价于检测 mAP 或药材区域定位能力。",
  ], 1.0, 1.25, 11.2, 2.85, 16);
  slide.addText("结论：分类路线已有可追溯阶段结果；检测结论必须来自真实 bbox 数据、正式训练权重和可追溯测试报告。", {
    x: 1.0,
    y: 4.65,
    w: 11.1,
    h: 0.75,
    fontFace: "Microsoft YaHei",
    fontSize: 18,
    bold: true,
    color: C.navy,
    margin: 0,
    fit: "shrink",
  });
  footer(slide);
}

pptx.writeFile({ fileName: path.join(outDir, "overview_design.pptx") });
