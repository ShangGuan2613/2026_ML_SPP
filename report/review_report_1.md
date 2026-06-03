# Review Report 1 - A/B 部分代码问题反馈 (2026_ML_SPP)

**日期**: 2026-06-03  
**Reviewer**: C 负责 (Grok 辅助分析)  
**项目阶段**: A/B 已基本完成代码与 notebooks，C 进入评估/交付阶段  
**审查范围**: 仅 A/B 部分（src/preprocess.py + notebooks 01/02 + test_preprocess + data/ + config.py + models.py + train.py + notebooks 03/04 + test_train + 相关共享）。**未审查 C 自己的 evaluate / test_evaluate / report / slides 实现细节**。  
**审查方式**: 静态代码阅读、notebook cell 结构解析、git 历史/文件对比、import & config 引用 grep、与 README 分工对照。**未执行任何可能改变 A/B 逻辑的修改**。

---

## 已完成的低影响修复 (Fixes Applied - 置于报告最前)

**原则**: 只修复**不影响 A/B 两个人核心工作**的事项。即：
- 不修改 `src/preprocess.py`、`src/config.py`、`src/models.py`、`src/train.py` 任何逻辑或接口。
- 不修改 `notebooks/0[1-4]_*.ipynb` 任何内容或 cell。
- 不修改 `tests/test_preprocess.py`、`tests/test_train.py` 的测试用例。
- 只动**共享文件**、**C 明确负责的 utils**、**缺失的文档占位符**、**目录结构**、**恢复之前 A/B 自己产生的已跟踪 artifacts**。

已修复并 git add 的内容如下（可通过 `git diff --cached` 或后续 PR 查看）：

1. **恢复 A/B 产出 artifacts（关键基础修复）**  
   执行 `git checkout -- data/raw data/processed outputs/models`。  
   - 恢复了 student-mat.csv / student-por.csv / student.txt（A 的原始数据）。  
   - 恢复了 X_*.csv / y_*.csv / preprocessor.pkl（A nb02 产生的 processed 数据，B 依赖）。  
   - 恢复了 12 个 classification_*.joblib + regression_*.joblib（B 训练并保存的模型，包括 _Tuned 版本）。  
   - 原因：review 时工作树显示大量 `D` 删除，这些是 A/B 历史交付物（见 commit e4fd7fe、ab29e01），不是源码。恢复后 C 才能基于真实数据/模型实现 evaluate，而不改变任何 A/B 写的代码。当前 git status 相关删除已消除。

2. **彻底清理并加固 .gitignore**  
   - 删除了三处重复/损坏的 "ML Project Specific" 块（原 101-124 行左右有重叠 + "logs/# ML Project Specific" 拼接错误）。  
   - 现在只保留一处干净的 ML 规则。  
   - 新增白名单例外，支持在被 ignore 的目录下安全跟踪结构文件：
     ```
     data/raw/
     !data/raw/.gitkeep
     !data/raw/data_description.md
     data/processed/
     !data/processed/.gitkeep
     !data/processed/processing_notes.md
     outputs/figures/ !... .gitkeep
     outputs/tables/ !... .gitkeep
     outputs/models/ !... .gitkeep
     logs/ !... .gitkeep
     ```
   - 这样未来 A/B/C 都可以干净地保留目录，而不会意外提交大 csv 或模型。

3. **补充 requirements.txt（原 0 字节）**  
   写入完整依赖（基于实际代码和 notebook import）：
   - pandas, numpy, scikit-learn, joblib (核心)
   - matplotlib, seaborn (可视化，nb01/02 大量使用)
   - pytest (测试)
   - jupyter/ipykernel 注释说明
   - 共享文件，所有人 pip install -r 即可复现。添加了项目注释。

4. **完善 src/utils.py（C 明确负责的部分）**  
   - 实现了 `ensure_dir(path)`（README 分工表里写明 "src/utils.py [C] 通用工具（set_seed、ensure_dir）"）。
   - 函数使用 `pathlib.Path.mkdir(parents=True, exist_ok=True)`，带中英文文档字符串。
   - 现在可被全项目统一调用：`from src import ensure_dir` 或 `from src.utils import ensure_dir`。
   - 当前 A/B 代码里还是手动 mkdir（train.py 里只做了 models 目录），此函数为未来对齐或 C 自己 evaluator 准备，不强制现在改 A/B 文件 → 零影响。

5. **更新 src/__init__.py（共享文件）**  
   - 新增导出：`from .utils import set_seed, ensure_dir`
   - 之前只导出了 Config/Preprocessor/Trainer 等，utils 工具一直不可见。现在 `from src import ensure_dir` 可用。低影响共享改进。

6. **创建/确保完整目录结构 + .gitkeep**  
   - `mkdir -p data/raw data/processed outputs/figures outputs/tables outputs/models logs report`
   - 在每个目录下放置 .gitkeep（内容带简短说明），并 `-f` add（配合 .gitignore 白名单）。
   - 保证 repo 里目录结构始终存在，即使内容被 ignore。

7. **补齐 A 部分缺失的占位文档（README 明确标注由 A 负责，但从未创建）**  
   - `data/raw/data_description.md`：数据集来源、文件说明、G3 目标描述 + 指向 `student.txt` 的完整属性表。  
   - `data/processed/processing_notes.md`：记录了两套预处理路径的差异、已知问题（Unnamed:0、fit 时机、格式不兼容等）、B 依赖情况。纯文档，不改 A 任何代码。
   - 这些文件已用 `!` 规则白名单 + add。

8. **其他微调**  
   - 确保 report/ 目录存在（C 后续 final_report 用）。  
   - 以上所有修复均已 `git add`（状态包含 M .gitignore / requirements.txt / src/utils.py / src/__init__.py + A 新文件）。

**影响评估**：以上操作**完全不改变 A/B 的算法逻辑、接口签名、notebook 执行结果、测试断言**。A/B 继续改他们的文件时不会冲突。C 现在有更完整的结构和依赖可直接开始工作。

---

## A 部分问题反馈（数据与预处理）- 按优先级排序

### P0（阻塞性，必须 A 优先处理，否则 B/C 无法可靠交付）

- **processed 数据输出带 "Unnamed: 0" 垃圾列，直接污染 B 的模型训练输入**  
  nb02 在保存时：
  ```python
  X_train_df = pd.DataFrame(..., index=X_train.index)
  X_train_df.to_csv("../data/processed/X_train.csv")  # 默认 index=True
  ```
  导致第一列 "Unnamed: 0"（原始 0~394 的 index 值）被当成特征。B 的 nb03/04 直接 read_csv 后使用，X 实际 42 列含噪声。  
  证据：`python -c` 解析 git show HEAD:data/processed/X_train.csv 确认。  
  **位置**: notebooks/02_preprocessing.ipynb（保存处理后数据那一段）  
  **影响**: 所有 B 模型可能学到无意义特征；C 后续评估也会受影响。**强烈建议 A 立即修**（加 index=False）并重新生成 processed 数据。

- **A 的官方 Preprocessor 类与 A 自己写的 notebooks 完全脱节**  
  - `notebooks/01_data_exploration.ipynb` 和 `02_preprocessing.ipynb` **零次 import 或调用** `from src.preprocess import Preprocessor`。
  - nb02 完全 duplicate 了一套自己的预处理逻辑（动态 numeric/cat 选择、clip absences 而非 row filter、fit_transform 在 split 之后、保存 csv+pkl 而非 npz）。
  - B notebooks 03/04 只能消费 nb02 产出的 csv，不能使用 src 里的 "官方" 流程。
  - **位置**: notebooks/02_preprocessing.ipynb（几乎整文件）、src/preprocess.py（整个类但没人用）。  
  **README 阶段依赖**: A 应该先写 preprocess.py，B 依赖 A 的输出。这里 A 自己内部也没对齐。

- **data/ 相关占位文件长期缺失**（现已由 C 补齐文档，但 A 应负责维护）  
  - README 明确：`data/raw/data_description.md`、`data/processed/processing_notes.md` 由 A 负责。
  - git 历史和 review 时完全没有这两个文件（只有 student.txt 和 nb02 产出的 csv/pkl）。
  - 现已创建占位 + 内容，放在 review 最前面的修复里。

- **当前工作树曾缺失 A/B 全部数据/模型 artifacts**（已 restore 缓解）  
  review 开始时 `find data outputs` 为空，git status 大量 `D`。虽然历史里有（commit e4fd7fe 添加数据集），但 WT 不可用。C 无法基于空数据写 evaluate。已通过 checkout 恢复。

### P1（高优先 - 实现质量、泄露、测试、结构）

- **src/preprocess.py 实现存在多处设计/正确性问题**（A 核心代码）：
  - `encode_categorical` (55-72)：只 fit ColumnTransformer，**return df_encoded 仍是原始未编码 df**（copy of clean）。注释说“类别特征独热编码”，实际没做。
  - `run_pipeline` (117-158)：`df_encoded = encode...` 后立即 `X, y = split_features_target(df_encoded...)`，此时 X 仍含字符串类别列；split 后再调用 `scale_features` 才真正 transform。返回的 dict["X"] / ["feature_names"] 都是 one-hot **之前**的。
  - **数据泄露风险**：preprocessor.fit 在 `df_clean`（全量）上执行，`train_test_split` 在后。数值 scaler 是在 scale 里只 fit train，但 one-hot categories 是全量看到的。
  - `scale_features` 里总是先 preprocessor.transform 再 scaler。
  - `save_processed` (160)：直接 np.savez，不调用 ensure_dir（当时 utils 也没实现）。
  - `clean` 逻辑与 nb02 不同（row filter vs quantile clip）。
  - **位置**: src/preprocess.py 全文件（尤其是 __init__ 18-31 硬编码特征、encode 59-70、run 125-145、scale 107-113）。

- **notebooks 01/02 结构极差，几乎不可作为可复现文档**：
  - 总 cell 数极少（01: 4 cells，02: 5 cells）。
  - 几乎所有内容塞在**一个巨大的 code cell** 里，用 `# %% [markdown]` + code 混排的 jupytext 格式。
  - 有多个空 cell。
  - 不是标准的 "每个步骤一个 cell + markdown 说明 + 执行输出" 的探索 notebook。
  - 位置: notebooks/01_data_exploration.ipynb, notebooks/02_preprocessing.ipynb（解析 cell 结构得到）。

- **tests/test_preprocess.py 完全空白**：
  - 只有 `class TestPreprocessor: pass`。
  - A 负责的测试框架没落地（README 明确列出）。
  - 对比 B 的 test_train.py 至少有 3 个有意义的测试。

- **硬编码 vs Config**：
  - nb02 里 `train_test_split(..., test_size=0.2, random_state=42)` 完全没用 `Config.TEST_SIZE / RANDOM_SEED`。
  - preprocess.py 自己倒是用了 config，但 nbs 没消费。

- **目录创建不统一**：
  - nb01/02 里散落 `os.makedirs("../outputs/figures", exist_ok=True)` 和 processed。
  - Preprocessor/Trainer 部分有 mkdir，部分没有。
  - （现已提供 ensure_dir 工具）。

### P2（中低优先 - 文档、历史、其他）

- data/raw/ 实际提交的是 student.txt 而非 README 要求的 data_description.md（现已补）。
- nb01/02 尝试保存 figure，但 outputs/figures 当时不存在 + gitignored，实际没持久化到 repo（C 负责后续）。
- 没有端到端脚本演示 "用 Preprocessor 产生数据 → B 消费" 的标准路径。
- student-por.csv 存在但完全没用（只有 mat 被消费）。

---

## B 部分问题反馈（模型构建与训练）- 按优先级排序

### P0（阻塞性 / 语义不一致，强烈建议 B 立即澄清）

- **03_classification_models.ipynb 的分类任务定义与自身文档、报告预期完全不符（最严重问题）**：
  - 文件顶部的 markdown header 明确写：
    > "预测学生是否通过 / 成绩等级"
  - 实际代码：
    ```python
    y_train = pd.read_csv('data/processed/y_train.csv').iloc[:, -1].values.ravel()
    ... 
    models = {"LogisticRegression": trainer.train_model(..., task="classification"), ...}
    # 直接把 G3 (0-20) 当 label
    cv_res = cross_validate(..., scoring=['accuracy', 'precision_weighted', ...])
    y_pred_cv = cross_val_predict(...)
    cm = confusion_matrix(y_train, y_pred_cv)  # 可能是 18x18
    ```
  - 从恢复的数据看：y unique ~18 个，范围 0-20。完全是把回归目标当多分类问题在做，没有 pass/fail（G3>=10）或 5 等级 binning。
  - 这导致：
    - 混淆矩阵、ROC micro 对业务无意义。
    - 和 report/final_report.md 里 "分类模型" 一节（Accuracy/Precision/Recall/F1 + 混淆矩阵 + 最佳模型选择）描述不匹配。
    - 和 README 里 "分类模型训练与对比" 的语义不符。
  - **位置**: notebooks/03_classification_models.ipynb（header + "3. 训练 5 大基础分类器" + "5. 生成四大指标表格" + ROC 部分）。
  - **建议 B**：要么改 header，要么（推荐）在 notebook 里先把 G3 离散化成 "pass/fail" 或 "等级" 再训练分类器。否则整个 "分类" 部分对 C 的报告都是错的。

- B 虽然保存了模型（命名规范），但因为上面问题，"分类模型" 的实际意义存疑。

### P1（高优先 - 配置未用、测试缺失、结构）

- **config.py 定义的超参数大量闲置**：
  - TREE_PARAMS、SVM_PARAMS、KNN_PARAMS 写了，但 nb03/04 只传了 RF_PARAMS（classif）和 RIDGE_LASSO_PARAMS（reg）。
  - VAL_SIZE = 0.1 完全没人用（项目里没有 validation split 逻辑，preprocess 只有 test split）。
  - 模型列表也没放在 config（factories 里硬编码，nbs 又自己写了 dict）。
  - **位置**: src/config.py:18-44（注释 "按 README 规范补齐"）；notebooks/03...80 行, 04...79 行只用两个。
  - 建议 B 把 grid search 扩展到其他模型，或至少在 notebook 里展示如何用 config 里的 grid。

- **tests/test_train.py 测试覆盖明显不足**：
  - 只测了 LogisticRegression + LinearRegression 的基础 train。
  - 只测了一个 RandomForest 的 save/load。
  - **完全没有**：
    - `train_with_grid_search` 的测试。
    - 工厂里其他 8 个模型。
    - 非法 model_name 的异常测试（Trainer / Factory 应该抛 ValueError）。
    - 使用 Config 里 params 的测试。
  - **位置**: tests/test_train.py（fixture + 3 个 def test_）。

- **notebooks 03/04 结构问题与 A 相同**：
  - 同样 crammed 进 1 个大 code cell + 少量空 cell。
  - 硬编码路径 `pd.read_csv('data/processed/X_train.csv')`、random_state=42、test_size（虽然数据已 split 好）。
  - 画图只 `plt.show()`，没有 `savefig` 到 outputs/figures/（C 后面要引用）。
  - 没有把 df_compare 指标保存到 outputs/tables/（C 需要的交付物）。
  - 位置: notebooks/03_classification_models.ipynb 和 04_regression_models.ipynb。

### P2（中优先）

- 只对 "冠军" 模型（RF / Ridge）做了 grid search，其他 4 个模型只训 base 版就保存了。
- nbs 里 `display(df_compare)` 依赖 IPython，在纯脚本环境会失败。
- 虽然 Trainer 支持 GridSearchCV + n_jobs=-1，但 nbs 没有充分利用（比如可以对多个模型循环 grid）。
- 加载数据后没清理 Unnamed: 0（根因 A，但 B 消费方也该防御）。
- train.py 里 `_get_model_instance` 做了 random_state 安全设置，设计不错，但 grid search 时 base_model 创建后 grid 会 override params。

### P3（低优先 / 观察）

- models.py 严格实现了 5+5 个（Classifier 含 SVM/KNN，Regressor 不含），与 docstring "严格按照 README 要求" 一致。OK。
- 部分模型（LogisticRegression、SVM）在默认参数下可能收敛警告或慢，nbs 没设置 max_iter / tol 等。
- 历史有 "chore: 强制上传 outputs 模型文件" commit，现在通过 gitignore + .gitkeep 管理更规范（已修复）。
- 没有在 Trainer 里提供 "train_all" + "grid_all" 的便捷方法，nbs 自己写了重复代码。

---

## 对 C 后续工作的影响与建议（简要）

- 现在数据/模型已恢复、目录结构完整、requirements 可用、ensure_dir 已就位 → C 可以开始写 `src/evaluate.py` 了（加载 processed test + B 的 joblib 模型，计算指标，plot 并保存到 outputs/figures + outputs/tables）。
- 强烈建议在实现 evaluate 前，和 A/B 确认：
  - 最终用哪套 processed 数据（csv 还是 npz）？
  - 分类任务到底是 pass/fail 还是 multi-class G3？（否则 report 里的分类章节会很尴尬）
- 报告和 slides 里要引用 outputs/ 里的东西，建议等 C 的 evaluator 跑出稳定 artifacts 后再写。
- 已创建的 processing_notes.md 里记录了很多 A/B 脱节点，可作为 C 写报告时的 "实验设置" 参考。

---

**审查结束**。此 report 已写入 `review_report_1.md`（根目录）。  
所有修复已 git add，可在下次 commit 时一起提交（或单独）。  
如果 A/B 看到后有异议或想讨论具体行号问题，欢迎直接回复或开 issue。

**下一步（C 自己）**：开始实现 evaluate.py + test_evaluate.py + 利用已恢复的数据生成 figures/tables，然后写 final_report 和 pptx。

（本报告内容全部基于实际工具检查结果，未凭空推测。）
