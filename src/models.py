from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

class ClassifierFactory:
    """分类模型工厂：严格按照 README 要求提供 5 个分类器"""
    _models = {
        "LogisticRegression": LogisticRegression,
        "DecisionTree": DecisionTreeClassifier,
        "RandomForest": RandomForestClassifier,
        "SVM": SVC,
        "KNN": KNeighborsClassifier
    }

    @classmethod
    def get(cls, name: str, **kwargs):
        if name not in cls._models:
            raise ValueError(f"分类器 '{name}' 不支持。当前支持: {cls.available()}")
        return cls._models[name](**kwargs)

    @classmethod
    def available(cls) -> list[str]:
        return list(cls._models.keys())


class RegressorFactory:
    """回归模型工厂：严格按照 README 要求提供 5 个回归器"""
    _models = {
        "LinearRegression": LinearRegression,
        "Ridge": Ridge,
        "Lasso": Lasso,
        "DecisionTree": DecisionTreeRegressor,
        "RandomForest": RandomForestRegressor
    }

    @classmethod
    def get(cls, name: str, **kwargs):
        if name not in cls._models:
            raise ValueError(f"回归器 '{name}' 不支持。当前支持: {cls.available()}")
        return cls._models[name](**kwargs)

    @classmethod
    def available(cls) -> list[str]:
        return list(cls._models.keys())