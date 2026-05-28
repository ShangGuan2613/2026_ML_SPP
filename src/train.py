# src/train.py
import joblib
from pathlib import Path
from sklearn.model_selection import GridSearchCV

from .config import Config
from .utils import set_seed
from .models import ClassifierFactory, RegressorFactory


class Trainer:
    def __init__(self, config: Config = None):
        self.config = config or Config()
        set_seed(self.config.RANDOM_SEED)

        # 确保输出模型的目录存在，防止保存时报错找不到文件夹
        self.config.OUTPUTS_MODELS.mkdir(parents=True, exist_ok=True)

    def _get_model_instance(self, model_name: str, task: str, **kwargs):
        """内部辅助方法：根据任务类型获取模型实例，并安全地统一设置随机种子"""

        # 第一步：干净地实例化模型，不强塞任何参数
        if task == "classification":
            model = ClassifierFactory.get(model_name, **kwargs)
        elif task == "regression":
            model = RegressorFactory.get(model_name, **kwargs)
        else:
            raise ValueError("Task 必须是 'classification' 或 'regression'")

        # 第二步：安全检查。如果该模型支持 random_state（比如随机森林、逻辑回归），才进行设置。
        # 不支持的（比如 KNN、线性回归）就直接跳过，防止报 TypeError。
        if hasattr(model, 'random_state') and 'random_state' not in kwargs:
            model.set_params(random_state=self.config.RANDOM_SEED)

        return model

    def train_model(self, model_name: str, X_train, y_train, task: str = "classification", **kwargs):
        """训练基础模型"""
        model = self._get_model_instance(model_name, task, **kwargs)
        model.fit(X_train, y_train)
        print(f"[{model_name}] 基础模型训练完成。")
        return model

    def train_with_grid_search(self, model_name: str, X_train, y_train, param_grid: dict, task: str = "classification",
                               cv: int = 5):
        """使用网格搜索寻找最优超参数并训练"""
        base_model = self._get_model_instance(model_name, task)

        print(f"[{model_name}] 开始进行网格搜索调参...")
        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=param_grid,
            cv=cv,
            n_jobs=-1,  # 开启所有 CPU 核心并行搜索，加快速度
            verbose=1  # 打印搜索进度
        )
        grid_search.fit(X_train, y_train)

        print(f"[{model_name}] 网格搜索最佳参数: {grid_search.best_params_}")
        print(f"[{model_name}] 最佳交叉验证得分: {grid_search.best_score_:.4f}")

        # 返回使用最佳参数并在整个训练集上重新拟合好的模型
        return grid_search.best_estimator_

    def save_model(self, model, model_name: str, task: str = "classification"):
        """将训练好的模型持久化保存为 joblib 文件"""
        filename = f"{task}_{model_name}.joblib"
        save_path = self.config.OUTPUTS_MODELS / filename
        joblib.dump(model, save_path)
        print(f"✅ 模型已成功保存至: {save_path}")

    def load_model(self, model_name: str, task: str = "classification"):
        """加载已保存的模型文件"""
        filename = f"{task}_{model_name}.joblib"
        load_path = self.config.OUTPUTS_MODELS / filename

        if not load_path.exists():
            raise FileNotFoundError(f"❌ 找不到模型文件: {load_path}")

        model = joblib.load(load_path)
        print(f"🔄 成功从 {load_path} 加载模型。")
        return model