from pathlib import Path

import pandas as pd

from .config import Config


class Evaluator:
    def __init__(self, config: Config = None):
        self.config = config or Config()

    def classification_metrics(self, y_true, y_pred, y_prob=None) -> dict:
        pass

    def regression_metrics(self, y_true, y_pred) -> dict:
        pass

    def plot_confusion_matrix(self, y_true, y_pred, labels: list[str] = None, title: str = "Confusion Matrix"):
        pass

    def plot_feature_importance(self, model, feature_names: list[str], title: str = "Feature Importance", top_n: int = 20):
        pass

    def generate_report(self, metrics: dict, model_name: str, task: str) -> Path:
        pass
