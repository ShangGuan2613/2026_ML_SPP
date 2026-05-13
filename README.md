# 2026_ML_SPP

学生成绩预测项目 — 2026 机器学习期末项目

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
  04_regression_models.ipynb           [B]

src/
  __init__.py                           共享（统一导出）
  config.py                           [B]
  utils.py                            [C]
  preprocess.py                       [A]
  models.py                           [B]
  train.py                            [B]
  evaluate.py                         [C]

outputs/
  models/                             [B]  训练好的 .joblib 模型文件
  figures/                            [C]  生成的图表
  tables/                             [C]  评估指标 CSV

report/
  final_report.md                     占位文件 → [C] 负责撰写 final_report.docx

slides/
  final_presentation.md               占位文件 → [C] 负责制作 final_presentation.pptx

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

**角色**: 数据工程师

| 文件 | 说明 |
|------|------|
| `data/raw/` | 收集并放置原始学生成绩 CSV |
| `data/processed/` | 运行预处理后保存清洗数据 |
| `src/preprocess.py` | 实现 Preprocessor 类（加载、清洗、编码、切分、缩放） |
| `notebooks/01_data_exploration.ipynb` | 数据探索与可视化（分布、相关性、缺失值等） |
| `notebooks/02_preprocessing.ipynb` | 数据预处理流程展示与验证 |
| `tests/test_preprocess.py` | 为 Preprocessor 编写单元测试 |

### B — 模型构建与训练

**角色**: 算法工程师

| 文件 | 说明 |
|------|------|
| `src/config.py` | 配置管理（路径常量、模型列表、超参数空间等） |
| `src/models.py` | 模型工厂（ClassifierFactory + RegressorFactory） |
| `src/train.py` | 训练器（单模型训练、GridSearch、保存/加载） |
| `notebooks/03_classification_models.ipynb` | 分类模型训练与对比 |
| `notebooks/04_regression_models.ipynb` | 回归模型训练与对比 |
| `outputs/models/` | 保存训练好的模型文件 |
| `tests/test_train.py` | 为 Trainer 编写单元测试 |

### C — 评估、测试与交付

**角色**: 评估与交付工程师

| 文件 | 说明 |
|------|------|
| `src/utils.py` | 通用工具（set_seed、ensure_dir） |
| `src/evaluate.py` | 评估器（指标计算、图表生成、CSV 导出） |
| `tests/` | 搭建测试框架，为 Evaluator 编写单元测试 |
| `outputs/figures/` | 负责从 evaluator 导出图表 |
| `outputs/tables/` | 负责从 evaluator 导出指标表格 |
| `report/final_report.docx` | 撰写最终报告 |
| `slides/final_presentation.pptx` | 制作演示文稿 |

### 共享文件

| 文件 | 说明 |
|------|------|
| `src/__init__.py` | 共同协商统一导入接口 |
| `requirements.txt` | 各自添加需要的库 |
| `.gitignore` | 共同维护 |


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
Phase 2-B:  src/config.py      ← B 定义模型列表和超参数
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
             所有人共同校对付最终交付物
```

### 依赖关系图

```
A (preprocess) ──→ B (modeling) ──→ C (evaluation) ──→ 报告/演示
                     ↑                    ↑
                     └──── utils.py ──────┘ (C 负责，所有人用)
```

## 关键约定

1. **接口协商**: 每个阶段开始前，上下游先对齐函数签名和数据格式
2. **提交粒度**: 每完成一个函数或一个 Notebook 章节就做一次 commit
3. **互相 Review**: 阶段衔接处做一次代码审查，确保上下游接口一致
