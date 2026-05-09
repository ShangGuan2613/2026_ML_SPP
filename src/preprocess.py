import pandas as pd

from .config import Config
from .utils import set_seed


class Preprocessor:
    def __init__(self, config: Config = None):
        self.config = config or Config()
        set_seed(self.config.RANDOM_SEED)

    def load_raw(self, filename: str) -> pd.DataFrame:
        pass

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def encode_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def split_features_target(self, df: pd.DataFrame, target_col: str):
        pass

    def split_train_test(self, X, y):
        pass

    def scale_features(self, X_train, X_test):
        pass

    def run_pipeline(self, raw_filename: str, target_col: str, scale: bool = True) -> dict:
        pass
