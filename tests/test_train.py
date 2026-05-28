import pytest
import os
from sklearn.datasets import make_classification, make_regression
from src.config import Config
from src.train import Trainer


class TestTrainer:

    @pytest.fixture
    def clf_data(self):
        """生成用于分类的测试数据"""
        return make_classification(n_samples=100, n_features=5, random_state=42)

    @pytest.fixture
    def reg_data(self):
        """生成用于回归的测试数据"""
        return make_regression(n_samples=100, n_features=5, random_state=42)

    @pytest.fixture
    def trainer(self):
        """初始化 Trainer 实例"""
        return Trainer(Config())

    def test_train_classification_model(self, trainer, clf_data):
        X, y = clf_data
        model = trainer.train_model("LogisticRegression", X, y, task="classification")
        assert model is not None
        assert hasattr(model, "predict")

    def test_train_regression_model(self, trainer, reg_data):
        X, y = reg_data
        model = trainer.train_model("LinearRegression", X, y, task="regression")
        assert model is not None
        assert hasattr(model, "predict")

    def test_save_and_load_model(self, trainer, clf_data):
        X, y = clf_data
        # 1. 训练模型
        model = trainer.train_model("RandomForest", X, y, task="classification")

        # 2. 保存模型
        test_model_name = "test_rf_model"
        trainer.save_model(model, test_model_name, task="classification")

        expected_path = trainer.config.OUTPUTS_MODELS / f"classification_{test_model_name}.joblib"
        assert expected_path.exists()  # 断言文件确实被写入了磁盘

        # 3. 加载模型
        loaded_model = trainer.load_model(test_model_name, task="classification")
        assert hasattr(loaded_model, "predict")  # 断言加载出来的是个合法模型

        # 4. 清理测试产生的临时文件
        if expected_path.exists():
            os.remove(expected_path)
