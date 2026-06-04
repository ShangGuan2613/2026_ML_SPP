# 2026_ML_SPP

学生成绩预测项目 — 2026 机器学习期末项目

> **📢 期末展示材料（2026-06-10 @ N528，5分钟）**  
> 重点展示 **工作量 + 亮点** 。核心故事线：“G2（上一阶段成绩）是压倒性预测因子，揭示学业累积性 + 早期干预窗口”。
>
> ** 三件套（必须一起用，效果最佳）** ：
> 1. `report/2026_ML_SPP_Keynote.html` — 苹果发布会风格纯 HTML 演示稿（推荐直接用）
>    - 浏览器全屏打开（`open report/2026_ML_SPP_Keynote.html`）
>    - 键盘控制：→/空格 前进，← 后退，F 全屏，Esc 退出，D 直达交互 Demo
>    - 第 12 页内嵌真实可交互的风险预测器（滑块实时更新 + What-If 模拟）
> 2. `report/5分钟演讲稿_配HTML_Keynote.md` — 完整演讲稿（按幻灯片逐页写好说辞 + 时长 + Demo 操作细节，面向老师+同学）
> 3. `report/story.md` — 现场作战 playbook（精确时间轴、谁做什么、风险预案）
>
> ** 深度理解整个项目演进** （推荐老师/复现时阅读）：
> `report/项目穿透文档.md` —— 一步步穿透记录：
> - 数据怎么拿、最初什么样
> - 洞见怎么掘
> - 每个模块怎么写的、负责什么
> - 历史上最大的坑（数据泄露、Unnamed:0、分类任务定义错误、notebook/src 脱节等）
> - 怎么一步步优化修复 + 后期 baseline / cross-subject / predictor 创新实现细节
>
> 这些让项目在同类中脱颖而出：**严谨、可复现、有教育洞见、可落地**，而非只跑几个模型。

> ** 快速创新点总览** （A/B/C 共同）：
> - A: 特征工程（grade_trend 等 4 个可解释衍生特征） + 统一支持 mat/por 双数据集
> - B: 引入 GradientBoosting 现代集成 + 完整 grid 空间 + G2-only baseline 对比实验
> - C: **unbiased hold-out 协议** + G2 persistence baseline 量化 + **跨课程（mat→por）泛化测试** + **StudentRiskPredictor 实际应用 demo（what-if 干预模拟）** + 全面测试 + 模块化工程质量

---

## 📢 期末展示使用指南（6月 10 日 N528）

### 1. 推荐演示方式（最稳）
```bash
# 打开 HTML 演示稿（全屏推荐）
open report/2026_ML_SPP_Keynote.html
# 或
python -m http.server 8000
# 浏览器访问 http://localhost:8000/report/2026_ML_SPP_Keynote.html
```

** 键盘操作** （苹果风）：
- `→` / `空格` / `Enter`：下一页
- `←`：上一页
- `F`：入全屏
- `D`：直接跳到交互 Demo 页（第12页）
- `Esc`：退出全屏或结束

** 现场材料** ：
- 主讲人：拿着 `report/5分钟演讲稿_配HTML_Keynote.md` 对着念（已标注每页时长 + 说辞 + 动作）
- Demo 手：负责第 12 页滑块操作（演讲稿里有精确台词）
- 彩排时参考 `report/story.md`

### 2. 真实 Demo 命令（强烈建议现场跑一次作为加分）
```bash
python -m src.predict
```

### 3. 复现全部 artifacts（老师/同学想看时）
详见 `report/项目穿透文档.md` 末尾的推荐命令，或直接运行 notebooks + `python -c "from src.evaluate import Evaluator; ..."`

---

## 项目结构（含分工标注）

```
data/                                    [A]
  raw/
    data_description.md                  占位文件 → A 负责收集原始 CSV
  processed/
    processing_notes.md                  占位文件 → A 负责保存处理后数据

notebooks/
  01_data_exploration.ipynb            [A]
  02_preprocessing.ipynb               [A]
  03_classification_models.ipynb       [B]
  04_regression_models.ipynb       [B]

src/
  __init__.py                           共享（统一导出）
  config.py                           [B]  (+ GB_PARAMS, 模型列表)
  utils.py                            [C]
  preprocess.py                       [A]  (+ feature_engineer, por 支持)
  models.py                           [B]  (+ GradientBoosting)
  train.py                            [B]
  evaluate.py                         [C]  (+ G2 baseline, cross-subject, 泛化实验)
  predict.py                          [C]  (新增：StudentRiskPredictor 实际应用演示)

outputs/
  models/                             [B]  训练好的 .joblib 模型文件
  figures/                            [C]  生成的图表
  tables/                             [C]  评估指标 CSV

report/
  2026_ML_SPP_Keynote.html            **苹果风 HTML 演示稿（期末展示主工具）**
  5分钟演讲稿_配HTML_Keynote.md       **完整演讲稿（配 HTML 使用）**
  story.md                            **现场执行 playbook**
  项目穿透文档.md                     **项目完整实现穿透文档（推荐阅读）**
  final_report.md                     占位文件 → [C] 负责撰写 final_report.docx

slides/
  final_presentation.md               占位文件 → [C] 负责制作 final_presentation.pptx（可选）

tests/
  __init__.py                         [C]
  test_preprocess.py                  [A]
  test_train.py                       [B]
  test_evaluate.py                    [C]

requirements.txt                       共享
.gitignore                             共享
README.md                              共享
```

---

## 三人分工总览

### A — 数据与预处理

** 角色** ：数据工程师

| 文件 | 说明 |
|------|------|
| `data/raw/` | 收集并放置原始学生成绩 CSV（mat + por） |
| `data/processed/` | 运行预处理后保存清洗数据 |
| `src/preprocess.py` | 实现 Preprocessor 类（加载、清洗、编码、切分、缩放 + **feature_engineer** + por 支持） |
| `notebooks/01_data_exploration.ipynb` | 数据探索与可视化（分布、相关性、缺失值等） |
| `notebooks/02_preprocessing.ipynb` | 数据预处理流程展示与验证 |
| `tests/test_preprocess.py` | 为 Preprocessor 编写单元测试（含 fe + por） |

### B — 模型构建与训练

** 角色** ：算法工程师

| 文件 | 说明 |
|------|------|
| `src/config.py` | 配置管理（路径常量、模型列表、超参空间等 + **GB_PARAMS**） |
| `src/models.py` | 模型工厂（ClassifierFactory + RegressorFactory + **GradientBoosting**） |
| `src/train.py` | 训练器（单模型训练、GridSearch、保存/加载） |
| `notebooks/03_classification_models.ipynb` | 分类模型训练与对比 |
| `notebooks/04_regression_models.ipynb` | 回归模型训练与对比 |
| `outputs/models/` | 保存训练好的模型文件（含 GB） |
| `tests/test_train.py` | 为 Trainer 编写单元测试（含 factory 全模型 + GB） |

### C — 评估、测试与交付（持续增强）

** 角色** ：评估与交付工程师

| 文件 | 说明 |
|------|------|
| `src/utils.py` | 通用工具（set_seed、ensure_dir） |
| `src/evaluate.py` | 完整评估器（test set unbiased 评估 + G2 baseline 对比 + cross-subject 泛化 + run_full... ） |
| `src/predict.py` | ** 创新交付** ：StudentRiskPredictor（加载预处理+模型，一键预测 + what-if 干预模拟 + CLI demo） |
| `tests/test_evaluate.py` | 14+ 可靠测试（含真实数据 + 新 baseline/cross/predictor） |
| `outputs/figures/` | 故事化图表（cm/roc/diagnostics/fi + _test 版） |
| `outputs/tables/` | 最终 unbiased *_test_metrics.csv + 新实验对比 |
| `report/final_report.docx` | 叙事驱动最终报告（G2 主导 + 工程亮点 + 泛化实验 + 实际应用价值） |
| `report/5分钟演讲稿_配HTML_Keynote.md` | 完整演讲稿（按幻灯片顺序，标注说辞、时长、Demo 操作） |

** 共享文件** 

| 文件 | 说明 |
|------|------|
| `src/__init__.py` | 共同协商统一导入接口 |
| `requirements.txt` | 各自添加需要的库 |
| `.gitignore` | 共同维护 |

---

## 构建与写文件先后顺序

### 第一阶段（并行启动）

```
Phase 1-A:  src/preprocess.py  ← A 先写预处理核心
             notebooks/01_data_exploration.ipynb
             notebooks/02_preprocessing.ipynb

Phase 1-C:  src/utils.py       ← C 先写基础工具（被所有人依赖）
             tests/ 测试框架搭建
```

### 第二阶段（依赖 A 的输出）

```
Phase 2-B:  src/config.py      ← B 定义模型列表和超参空间
             src/models.py      ← B 实现模型工厂
             src/train.py       ← B 实现训练器
             说明：B 需要 A 处理好的数据来调试训练流程
```

### 第三阶段（依赖 A + B 的输出）

```
Phase 3-C:  src/evaluate.py    ← C 实现评估器
             说明：C 需要 B 训练好的模型 + A 处理好的数据来跑评估
             notebooks/ 中的结果汇总
             outputs/figures/ 导出图表
             outputs/tables/ 导出指标
```

### 第四阶段（收尾）

```
Phase 4:    report/final_report.docx    ← C 撰写报告
             slides/final_presentation.pptx ← C 制作演示
             所有人共同校对最终交付物
```

### 依赖关系图

```
A (preprocess) ——→ B (modeling) ——→ C (evaluation) ——→ 报告/演示
                     ↑                    ↑
                     └──── utils.py ─────────┘ (C 负责，所有人用)
```

## 关键约定

1. ** 接口协商** ：每个阶段开始前，上下游先对齐函数签名和数据格式
2. ** 提交粒度** ：每完成一个函数或一个 Notebook 章节就做一次 commit
3. ** 互相 Review** ：阶段接键处做一次代码审查，确保上下游接口一致
