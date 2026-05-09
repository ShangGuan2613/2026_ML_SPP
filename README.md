# 2026_ML_SPP

学生成绩预测项目 — 2026 机器学习期末项目

## 项目结构

```
data/
  raw/           原始数据（CSV）
  processed/     预处理后的数据
notebooks/
  01_data_exploration.ipynb       数据探索与可视化
  02_preprocessing.ipynb          数据预处理
  03_classification_models.ipynb  分类模型训练与评估
  04_regression_models.ipynb      回归模型训练与评估
src/
  __init__.py    包初始化
  config.py      全局配置（路径、超参数、随机种子）
  utils.py       通用工具函数（种子设置、目录创建）
  preprocess.py  数据预处理流水线
  models.py      模型工厂（分类/回归）
  train.py       模型训练与保存
  evaluate.py    模型评估与可视化
outputs/
  models/        训练好的模型文件（.joblib）
  figures/       图表输出
  tables/        评估指标 CSV
report/          最终报告
slides/          最终演示文稿
tests/           单元测试
```

## 使用流程

1. 将原始数据放入 `data/raw/`
2. 在 `notebooks/` 中按序号依次运行
3. `src/` 下的模块可在 Notebook 中 import 使用
