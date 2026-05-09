from .config import Config
from .utils import set_seed


class Trainer:
    def __init__(self, config: Config = None):
        self.config = config or Config()
        set_seed(self.config.RANDOM_SEED)

    def train_model(self, model_name: str, X_train, y_train, task: str = "classification", **kwargs):
        pass

    def train_with_grid_search(self, model_name: str, X_train, y_train, task: str = "classification"):
        pass

    def save_model(self, model, model_name: str, task: str = "classification"):
        pass

    def load_model(self, model_name: str, task: str = "classification"):
        pass
