const pptxgen = require("pptxgenjs");

// Create presentation
let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Research Team';
pres.title = '阶段报告 (2026-02-27)';

// Color palette - Midnight Executive theme
const COLORS = {
  primary: "1E2761",      // Deep navy
  secondary: "2E4A82",    // Medium blue
  accent: "4A90D9",       // Bright blue
  light: "E8F0F8",        // Light blue-gray
  white: "FFFFFF",
  text: "1E293B",         // Dark text
  muted: "64748B",        // Muted text
  highlight: "F59E0B"     // Orange highlight
};

// Helper for shadow (fresh object each time)
const makeShadow = () => ({ type: "outer", color: "000000", blur: 4, offset: 2, angle: 135, opacity: 0.15 });

// ============================================
// Slide 1: Title Slide
// ============================================
let slide1 = pres.addSlide();
slide1.background = { color: COLORS.primary };

// Title
slide1.addText("GNN Unlearning 攻击研究", {
  x: 0.5, y: 1.8, w: 9, h: 0.8,
  fontSize: 40, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "left", margin: 0
});

// Subtitle
slide1.addText("导师汇报版阶段报告", {
  x: 0.5, y: 2.6, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Arial",
  color: COLORS.accent, align: "left", margin: 0
});

// Date
slide1.addText("2026-02-27", {
  x: 0.5, y: 4.5, w: 9, h: 0.4,
  fontSize: 16, fontFace: "Arial",
  color: COLORS.muted, align: "left", margin: 0
});

// Decorative bar
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 2.4, w: 1.5, h: 0.06,
  fill: { color: COLORS.accent }
});

// ============================================
// Slide 2: 一句话结论
// ============================================
let slide2 = pres.addSlide();
slide2.background = { color: COLORS.light };

// Header bar
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8,
  fill: { color: COLORS.primary }
});
slide2.addText("0. 一句话结论", {
  x: 0.5, y: 0.15, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "left", margin: 0
});

// Main content box
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.2, w: 9, h: 3.8,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

// Accent bar
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.2, w: 0.08, h: 3.8,
  fill: { color: COLORS.accent }
});

// Key conclusion text
slide2.addText("当前实验体系已完成从「单点结果」到「端到端、跨维度、可解释评估」的升级", {
  x: 0.8, y: 1.5, w: 8.4, h: 0.8,
  fontSize: 18, fontFace: "Arial", bold: true,
  color: COLORS.text, align: "left", margin: 0
});

slide2.addText("在 950 runs 的覆盖下，我们确认了方法族差异；同时通过新引入的 Relative F1 Drop（以 k=5 random 为基线）澄清了 Shard-based 方法看似「变好」 的来源，并把「攻击效果」与「方法自身增益」分离开来。", {
  x: 0.8, y: 2.3, w: 8.4, h: 1.5,
  fontSize: 16, fontFace: "Arial",
  color: COLORS.text, align: "left", margin: 0
});

// Stats highlight
slide2.addText("950 runs", {
  x: 0.8, y: 4.0, w: 2, h: 0.5,
  fontSize: 28, fontFace: "Arial", bold: true,
  color: COLORS.accent, align: "left", margin: 0
});
slide2.addText("实验规模", {
  x: 0.8, y: 4.45, w: 2, h: 0.3,
  fontSize: 12, fontFace: "Arial",
  color: COLORS.muted, align: "left", margin: 0
});

// ============================================
// Slide 3: 端到端流程
// ============================================
let slide3 = pres.addSlide();
slide3.background = { color: COLORS.light };

// Header bar
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8,
  fill: { color: COLORS.primary }
});
slide3.addText("1. 端到端实验流程", {
  x: 0.5, y: 0.15, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "left", margin: 0
});

// Process steps
const steps = [
  { num: "01", title: "批量主实验", desc: "results/experiments/*" },
  { num: "02", title: "相对指标评估", desc: "eval_relative.py + results/relative/" },
  { num: "03", title: "副作用评估", desc: "results/collateral/ (gap, flip)" },
  { num: "04", title: "统计汇总与可视化", desc: "report/paper/sections/*" },
  { num: "05", title: "状态核查", desc: "exp_status_checker.py" }
];

steps.forEach((step, i) => {
  const y = 1.1 + i * 0.85;

  // Number circle
  slide3.addShape(pres.shapes.OVAL, {
    x: 0.5, y: y, w: 0.5, h: 0.5,
    fill: { color: COLORS.accent }
  });
  slide3.addText(step.num, {
    x: 0.5, y: y, w: 0.5, h: 0.5,
    fontSize: 14, fontFace: "Arial", bold: true,
    color: COLORS.white, align: "center", valign: "middle", margin: 0
  });

  // Content
  slide3.addText(step.title, {
    x: 1.2, y: y, w: 3, h: 0.35,
    fontSize: 16, fontFace: "Arial", bold: true,
    color: COLORS.text, align: "left", margin: 0
  });
  slide3.addText(step.desc, {
    x: 1.2, y: y + 0.35, w: 8, h: 0.3,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.muted, align: "left", margin: 0
  });
});

// Arrow
slide3.addText("↓", {
  x: 0.5, y: 5.0, w: 0.5, h: 0.4,
  fontSize: 20, color: COLORS.accent, align: "center", margin: 0
});

// ============================================
// Slide 4: 当前覆盖规模
// ============================================
let slide4 = pres.addSlide();
slide4.background = { color: COLORS.light };

// Header bar
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8,
  fill: { color: COLORS.primary }
});
slide4.addText("1. 当前覆盖规模（已完成）", {
  x: 0.5, y: 0.15, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "left", margin: 0
});

// Stats grid
const stats = [
  { label: "总实验量", value: "950 runs", color: COLORS.accent },
  { label: "MG-0/1/2", value: "270", color: COLORS.secondary },
  { label: "Ratio敏感性", value: "240", color: COLORS.secondary },
  { label: "P2-EXT", value: "360", color: COLORS.secondary }
];

stats.forEach((stat, i) => {
  const x = 0.5 + (i % 2) * 4.7;
  const y = 1.0 + Math.floor(i / 2) * 1.2;

  slide4.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 4.4, h: 1.0,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });

  slide4.addText(stat.value, {
    x: x + 0.2, y: y + 0.15, w: 4, h: 0.5,
    fontSize: 28, fontFace: "Arial", bold: true,
    color: stat.color, align: "left", margin: 0
  });
  slide4.addText(stat.label, {
    x: x + 0.2, y: y + 0.6, w: 4, h: 0.3,
    fontSize: 14, fontFace: "Arial",
    color: COLORS.muted, align: "left", margin: 0
  });
});

// Coverage details
slide4.addText("主维度覆盖", {
  x: 0.5, y: 3.5, w: 9, h: 0.4,
  fontSize: 16, fontFace: "Arial", bold: true,
  color: COLORS.text, align: "left", margin: 0
});

const dimensions = [
  "方法: GIF, GNNDelete, GraphEraser, IDEA, MEGU",
  "数据集: cora, citeseer | 模型: GCN, GAT, GIN",
  "比例: 0.01, 0.05, 0.10, 0.20 | 策略: random, degree, pagerank, tracin, im_v4, hybrid_v4",
  "Seeds: 42, 212, 722, 1337, 2024"
];

dimensions.forEach((dim, i) => {
  slide4.addText(dim, {
    x: 0.5, y: 3.95 + i * 0.4, w: 9, h: 0.35,
    fontSize: 13, fontFace: "Arial",
    color: COLORS.muted, align: "left", margin: 0
  });
});

// ============================================
// Slide 5: 算力限制下的方法决策
// ============================================
let slide5 = pres.addSlide();
slide5.background = { color: COLORS.light };

// Header bar
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8,
  fill: { color: COLORS.primary }
});
slide5.addText("2. 算力限制下的方法决策", {
  x: 0.5, y: 0.15, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "left", margin: 0
});

// IF Framework section
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.0, w: 4.4, h: 2.3,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.0, w: 0.08, h: 2.3,
  fill: { color: COLORS.accent }
});

slide5.addText("IF 框架: TracIn", {
  x: 0.75, y: 1.15, w: 4, h: 0.4,
  fontSize: 16, fontFace: "Arial", bold: true,
  color: COLORS.text, align: "left", margin: 0
});

slide5.addText([
  { text: "精确 IF 开销爆炸", options: { bullet: true, breakLine: true } },
  { text: "超大图可能到天/周/月级", options: { bullet: true, breakLine: true } },
  { text: "采用 TracIn（一阶 pseudo-IF）作为可执行替代", options: { bullet: true } }
], {
  x: 0.75, y: 1.6, w: 4, h: 1.5,
  fontSize: 13, fontFace: "Arial",
  color: COLORS.text, align: "left", margin: 0
});

// IM Framework section
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 5.1, y: 1.0, w: 4.4, h: 2.3,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 5.1, y: 1.0, w: 0.08, h: 2.3,
  fill: { color: COLORS.highlight }
});

slide5.addText("IM 框架: IM v4", {
  x: 5.35, y: 1.15, w: 4, h: 0.4,
  fontSize: 16, fontFace: "Arial", bold: true,
  color: COLORS.text, align: "left", margin: 0
});

slide5.addText([
  { text: "V0 时间: 652.97s", options: { bullet: true, breakLine: true } },
  { text: "V4 时间: 18.90s", options: { bullet: true, breakLine: true } },
  { text: "加速比: 34.55x", options: { bullet: true } }
], {
  x: 5.35, y: 1.6, w: 4, h: 1.0,
  fontSize: 13, fontFace: "Arial",
  color: COLORS.text, align: "left", margin: 0
});

// Performance box
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.5, w: 9, h: 1.5,
  fill: { color: COLORS.primary }
});

slide5.addText("性能提升", {
  x: 0.7, y: 3.65, w: 2, h: 0.4,
  fontSize: 14, fontFace: "Arial", bold: true,
  color: COLORS.accent, align: "left", margin: 0
});

slide5.addText("34.55x", {
  x: 0.7, y: 4.0, w: 2, h: 0.7,
  fontSize: 36, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "left", margin: 0
});

slide5.addText("加速比 (IM V0 → V4)\nspread 损失仅 1.26%", {
  x: 2.8, y: 4.0, w: 4, h: 0.7,
  fontSize: 14, fontFace: "Arial",
  color: COLORS.light, align: "left", margin: 0
});

// Future direction
slide5.addText("大图下一步: D-SSA/IMM (RR-set 系)", {
  x: 6.5, y: 4.3, w: 3.5, h: 0.4,
  fontSize: 12, fontFace: "Arial", italic: true,
  color: COLORS.accent, align: "right", margin: 0
});

// ============================================
// Slide 6: 新指标 Relative F1 Drop
// ============================================
let slide6 = pres.addSlide();
slide6.background = { color: COLORS.light };

// Header bar
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8,
  fill: { color: COLORS.primary }
});
slide6.addText("3. 新指标: Relative F1 Drop", {
  x: 0.5, y: 0.15, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "left", margin: 0
});

// Definition box
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.0, w: 9, h: 1.5,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

slide6.addText("指标定义", {
  x: 0.7, y: 1.1, w: 2, h: 0.35,
  fontSize: 14, fontFace: "Arial", bold: true,
  color: COLORS.accent, align: "left", margin: 0
});

slide6.addText("Baseline: F1̄_after(k=5, random)", {
  x: 0.7, y: 1.5, w: 8, h: 0.3,
  fontSize: 14, fontFace: "Consolas",
  color: COLORS.text, align: "left", margin: 0
});

slide6.addText("Relative F1 Drop = F1̄_after(k=5, random) - F1_after(ratio=0.05, attack)", {
  x: 0.7, y: 1.85, w: 8, h: 0.3,
  fontSize: 14, fontFace: "Consolas",
  color: COLORS.text, align: "left", margin: 0
});

// What it solves
slide6.addText("解决的问题", {
  x: 0.5, y: 2.7, w: 9, h: 0.4,
  fontSize: 16, fontFace: "Arial", bold: true,
  color: COLORS.text, align: "left", margin: 0
});

slide6.addText("它把「方法自身带来的性能漂移」从「攻击额外造成的损伤」里剥离出来，特别适用于解释 Shard-based 的反直觉现象。", {
  x: 0.5, y: 3.1, w: 9, h: 0.8,
  fontSize: 15, fontFace: "Arial",
  color: COLORS.text, align: "left", margin: 0
});

// Key insight box
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.0, w: 9, h: 1.0,
  fill: { color: COLORS.highlight },
  shadow: makeShadow()
});

slide6.addText("核心价值：区分「方法自带提升」vs 「攻击真实增益」", {
  x: 0.7, y: 4.25, w: 8.5, h: 0.5,
  fontSize: 16, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "center", margin: 0
});

// ============================================
// Slide 7: 深度分析 - 是否变好?
// ============================================
let slide7 = pres.addSlide();
slide7.background = { color: COLORS.light };

// Header bar
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8,
  fill: { color: COLORS.primary }
});
slide7.addText("4. 深度分析：是否变好？", {
  x: 0.5, y: 0.15, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "left", margin: 0
});

// Three improvement areas
const improvements = [
  { title: "实验体系变好", desc: "从单配置扩展到跨方法/数据/模型/ratio 完整矩阵，5-seed 完整" },
  { title: "工程效率变好", desc: "IM 选点端到端提速 34.55x，明确大图迁移路线 (D-SSA)" },
  { title: "解释力变好", desc: "Relative 指标准确判断「攻击有效」还是「方法本身增益」" }
];

improvements.forEach((item, i) => {
  const x = 0.5 + i * 3.1;

  slide7.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.0, w: 2.9, h: 1.8,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });

  // Number badge
  slide7.addShape(pres.shapes.OVAL, {
    x: x + 0.15, y: 1.1, w: 0.4, h: 0.4,
    fill: { color: COLORS.accent }
  });
  slide7.addText((i + 1).toString(), {
    x: x + 0.15, y: 1.1, w: 0.4, h: 0.4,
    fontSize: 14, fontFace: "Arial", bold: true,
    color: COLORS.white, align: "center", valign: "middle", margin: 0
  });

  slide7.addText(item.title, {
    x: x + 0.15, y: 1.6, w: 2.6, h: 0.4,
    fontSize: 14, fontFace: "Arial", bold: true,
    color: COLORS.text, align: "left", margin: 0
  });

  slide7.addText(item.desc, {
    x: x + 0.15, y: 2.0, w: 2.6, h: 0.7,
    fontSize: 11, fontFace: "Arial",
    color: COLORS.muted, align: "left", margin: 0
  });
});

// Shard-based analysis
slide7.addText("Shard-based「gap 提升」解释", {
  x: 0.5, y: 3.0, w: 9, h: 0.4,
  fontSize: 16, fontFace: "Arial", bold: true,
  color: COLORS.text, align: "left", margin: 0
});

slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.4, w: 9, h: 1.8,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

slide7.addText([
  { text: "绝对指标：GraphEraser 经常出现负 drop（越删越好）", options: { bullet: true, breakLine: true } },
  { text: "MG-0 cora/gcn/r=0.05: GraphEraser F1 Drop = -5.2% ± 2.7", options: { bullet: true, breakLine: true } },
  { text: "说明 Shard-based 本身存在「性能抬升效应」", options: { bullet: true, breakLine: true } },
  { text: "Relative 口径下仍可看到攻击产生额外影响", options: { bullet: true } }
], {
  x: 0.7, y: 3.55, w: 8.5, h: 1.5,
  fontSize: 13, fontFace: "Arial",
  color: COLORS.text, align: "left", margin: 0
});

// ============================================
// Slide 8: 方法族稳定性分析
// ============================================
let slide8 = pres.addSlide();
slide8.background = { color: COLORS.light };

// Header bar
slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8,
  fill: { color: COLORS.primary }
});
slide8.addText("4. 方法族稳定性结论", {
  x: 0.5, y: 0.15, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "left", margin: 0
});

// Method cards
const methods = [
  { name: "GNNDelete", status: "脆弱性最高", detail: "长期处于最高 relative/f1_drop 区间", color: "DC2626" },
  { name: "GIF/IDEA/MEGU", status: "整体更稳", detail: "攻击效果存在但幅度显著低于 GNNDelete", color: "059669" },
  { name: "GraphEraser", status: "需谨慎阐释", detail: "绝对「提升」与相对「攻击增益」并存", color: "D97706" }
];

methods.forEach((m, i) => {
  const y = 1.0 + i * 1.45;

  // Card
  slide8.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 9, h: 1.3,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });

  // Accent bar
  slide8.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 0.1, h: 1.3,
    fill: { color: m.color }
  });

  // Method name
  slide8.addText(m.name, {
    x: 0.8, y: y + 0.15, w: 3, h: 0.4,
    fontSize: 18, fontFace: "Arial", bold: true,
    color: COLORS.text, align: "left", margin: 0
  });

  // Status
  slide8.addText(m.status, {
    x: 3.5, y: y + 0.15, w: 2, h: 0.4,
    fontSize: 14, fontFace: "Arial", bold: true,
    color: m.color, align: "left", margin: 0
  });

  // Detail
  slide8.addText(m.detail, {
    x: 0.8, y: y + 0.7, w: 8.5, h: 0.5,
    fontSize: 13, fontFace: "Arial",
    color: COLORS.muted, align: "left", margin: 0
  });
});

// Key insight
slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.6, w: 9, h: 0.7,
  fill: { color: COLORS.primary }
});
slide8.addText("双层结论：绝对指标 + Relative 指标合起来，才能避免误判", {
  x: 0.7, y: 4.75, w: 8.5, h: 0.4,
  fontSize: 14, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "center", margin: 0
});

// ============================================
// Slide 9: 可视化图表
// ============================================
let slide9 = pres.addSlide();
slide9.background = { color: COLORS.light };

// Header bar
slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8,
  fill: { color: COLORS.primary }
});
slide9.addText("5. 可视化图表（可直接引用）", {
  x: 0.5, y: 0.15, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "left", margin: 0
});

// Figure references
const figures = [
  { num: "FIG-1", title: "泛化与方法族对比", path: "../../results/paper_figures/FIG-1_Generalization.png" },
  { num: "FIG-2", title: "Ratio 敏感性", path: "../../results/paper_figures/FIG-2_Scaling.png" },
  { num: "FIG-3", title: "全方法脆弱性谱", path: "../../results/paper_figures/FIG-3_Spectrum.png" },
  { num: "FIG-4", title: "统计显著性", path: "../../results/paper_figures/FIG-4_Significance.png" },
  { num: "FIG-5", title: "Relative vs Gap", path: "../../results/paper_figures/FIG-5_Collateral.png" }
];

figures.forEach((fig, i) => {
  const x = 0.5 + (i % 3) * 3.1;
  const y = 1.0 + Math.floor(i / 3) * 1.8;

  slide9.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 2.9, h: 1.6,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });

  // Placeholder visual
  slide9.addShape(pres.shapes.RECTANGLE, {
    x: x + 0.15, y: y + 0.15, w: 2.6, h: 0.9,
    fill: { color: COLORS.light }
  });
  slide9.addText("📊", {
    x: x + 0.15, y: y + 0.15, w: 2.6, h: 0.9,
    fontSize: 32, align: "center", valign: "middle", margin: 0
  });

  slide9.addText(fig.num, {
    x: x + 0.15, y: y + 1.15, w: 1, h: 0.3,
    fontSize: 12, fontFace: "Arial", bold: true,
    color: COLORS.accent, align: "left", margin: 0
  });
  slide9.addText(fig.title, {
    x: x + 0.15, y: y + 1.4, w: 2.6, h: 0.15,
    fontSize: 11, fontFace: "Arial",
    color: COLORS.muted, align: "left", margin: 0
  });
});

// ============================================
// Slide 10: 简要结论
// ============================================
let slide10 = pres.addSlide();
slide10.background = { color: COLORS.primary };

// Title
slide10.addText("6. 面向下一次组会的简要结论", {
  x: 0.5, y: 0.5, w: 9, h: 0.6,
  fontSize: 28, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "left", margin: 0
});

// Decorative bar
slide10.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 1.5, h: 0.06,
  fill: { color: COLORS.accent }
});

// Three conclusions
const conclusions = [
  { num: "1", text: "已经把「攻击有效性」从「方法自身偏置」里分离出来（Relative + k=5 baseline）" },
  { num: "2", text: "IF 与 IM 的算力路径已明确：TracIn（当前可执行）+ IM v4（当前高效）+ D-SSA（大图下一步）" },
  { num: "3", text: "关键发现：Shard-based「变好」主要来自方法本身机制；但 Relative 口径下攻击增益并非 0，需明确「双层结论」" }
];

conclusions.forEach((c, i) => {
  const y = 1.5 + i * 1.2;

  // Number circle
  slide10.addShape(pres.shapes.OVAL, {
    x: 0.5, y: y, w: 0.5, h: 0.5,
    fill: { color: COLORS.accent }
  });
  slide10.addText(c.num, {
    x: 0.5, y: y, w: 0.5, h: 0.5,
    fontSize: 18, fontFace: "Arial", bold: true,
    color: COLORS.white, align: "center", valign: "middle", margin: 0
  });

  // Text
  slide10.addText(c.text, {
    x: 1.2, y: y + 0.05, w: 8.3, h: 0.9,
    fontSize: 16, fontFace: "Arial",
    color: COLORS.white, align: "left", margin: 0
  });
});

// ============================================
// Slide 11: 待补证据
// ============================================
let slide11 = pres.addSlide();
slide11.background = { color: COLORS.light };

// Header bar
slide11.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8,
  fill: { color: COLORS.primary }
});
slide11.addText("7. 待补证据（建议带给导师）", {
  x: 0.5, y: 0.15, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "left", margin: 0
});

// Evidence items
const evidence = [
  { title: "MIA 审计未闭环", desc: "按 paper_analysis.md 建议先补 GNNDelete + GIF 的最小对照" },
  { title: "机制验证缺 ablation", desc: "优先补 GNNDelete (DEC/NI) 最小分解实验" },
  { title: "外推证据不足", desc: "若做下一轮扩展，优先加 1 个更大规模数据集验证趋势是否保真" }
];

evidence.forEach((e, i) => {
  const y = 1.1 + i * 1.4;

  // Card
  slide11.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 9, h: 1.2,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });

  // Number badge
  slide11.addShape(pres.shapes.OVAL, {
    x: 0.7, y: y + 0.35, w: 0.5, h: 0.5,
    fill: { color: COLORS.highlight }
  });
  slide11.addText((i + 1).toString(), {
    x: 0.7, y: y + 0.35, w: 0.5, h: 0.5,
    fontSize: 18, fontFace: "Arial", bold: true,
    color: COLORS.white, align: "center", valign: "middle", margin: 0
  });

  // Title
  slide11.addText(e.title, {
    x: 1.4, y: y + 0.2, w: 8, h: 0.4,
    fontSize: 16, fontFace: "Arial", bold: true,
    color: COLORS.text, align: "left", margin: 0
  });

  // Description
  slide11.addText(e.desc, {
    x: 1.4, y: y + 0.65, w: 8, h: 0.4,
    fontSize: 14, fontFace: "Arial",
    color: COLORS.muted, align: "left", margin: 0
  });
});

// ============================================
// Slide 12: Thank You
// ============================================
let slide12 = pres.addSlide();
slide12.background = { color: COLORS.primary };

slide12.addText("谢谢！", {
  x: 0.5, y: 2.0, w: 9, h: 1,
  fontSize: 48, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "center", margin: 0
});

slide12.addText("Q & A", {
  x: 0.5, y: 3.2, w: 9, h: 0.6,
  fontSize: 24, fontFace: "Arial",
  color: COLORS.accent, align: "center", margin: 0
});

// Save
pres.writeFile({ fileName: "H:/project/OpenGU/GULib-master/report/paper/stage_report_2026-02-27.pptx" })
  .then(() => console.log("Presentation created successfully!"))
  .catch(err => console.error(err));
