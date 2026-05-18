import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

from .config import Config
from .utils import set_seed

class Preprocessor:
    def __init__(self, config: Config = None):
        # 初始化预处理类
        self.config = config or Config()
        set_seed(self.config.RANDOM_SEED)

        # 识别类别特征与数值特征
        self.categorical_features = [
            'school', 'sex', 'address', 'famsize', 'Pstatus',
            'Mjob', 'Fjob', 'reason', 'guardian',
            'schoolsup', 'famsup', 'paid', 'activities',
            'nursery', 'higher', 'internet', 'romantic'
        ]
        self.numeric_features = [
            'age', 'Medu', 'Fedu', 'traveltime', 'studytime',
            'failures', 'famrel', 'freetime', 'goout',
            'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2'
        ]
        # 预处理工具
        self.scaler = StandardScaler()
        self.preprocessor = None

    def load_raw(self, filename: str) -> pd.DataFrame:
        # 加载原始CSV数据
        file_path = self.config.DATA_RAW / filename
        df = pd.read_csv(file_path, sep=';')  # 学生数据分隔符为分号
        return df

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        # 数据清洗
        df_clean = df.copy()

        # 1. 删除重复行
        df_clean = df_clean.drop_duplicates()

        # 2. 异常值过滤（业务规则）
        df_clean = df_clean[
            (df_clean['age'] >= 15) & (df_clean['age'] <= 22) &  # 年龄15-22
            (df_clean['G3'] >= 0) & (df_clean['G3'] <= 20) &  # 成绩0-20
            (df_clean['failures'] >= 0)  # 挂科次数非负
            ]

        return df_clean

    def encode_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        # 类别特征独热编码
        df_encoded = df.copy()

        # 构建编码流水线：类别特征OneHot，数值特征保留
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'),
                 self.categorical_features),
                ('num', 'passthrough', self.numeric_features)
            ]
        )

        # 拟合编码
        feature_cols = self.categorical_features + self.numeric_features
        self.preprocessor.fit(df_encoded[feature_cols])

        return df_encoded

    def split_features_target(self, df: pd.DataFrame, target_col: str):
        """
        分离特征X与目标变量y
        df: 编码后DataFrame
        target_col: 目标列名（默认G3）
        return: X(特征), y(目标)
        """

        X = df.drop(columns=[target_col])
        y = df[target_col]
        return X, y

    def split_train_test(self, X, y):
        """
        划分训练集/测试集
        X: 特征
        y: 目标变量
        return: X_train, X_test, y_train, y_test
        """
        return train_test_split(
            X, y,
            test_size=self.config.TEST_SIZE,
            random_state=self.config.RANDOM_SEED,
            shuffle=True
        )

    def scale_features(self, X_train, X_test):
        """
        特征标准化
        X_train: 训练集特征
        X_test: 测试集特征
        return: 标准化后的X_train_scaled, X_test_scaled
        """
        # 先做独热编码
        X_train_encoded = self.preprocessor.transform(X_train)
        X_test_encoded = self.preprocessor.transform(X_test)

        # 标准化
        X_train_scaled = self.scaler.fit_transform(X_train_encoded)
        X_test_scaled = self.scaler.transform(X_test_encoded)

        return X_train_scaled, X_test_scaled

    def run_pipeline(self, raw_filename: str, target_col: str, scale: bool = True) -> dict:
        """
        预处理
        raw_filename: 原始数据文件名
        target_col: 目标列名
        scale: 是否标准化
        return: 包含所有处理结果的字典
        """
        # 1. 加载原始数据
        df_raw = self.load_raw(raw_filename)

        # 2. 数据清洗
        df_clean = self.clean(df_raw)

        # 3. 类别编码
        df_encoded = self.encode_categorical(df_clean)

        # 4. 分离特征与目标
        X, y = self.split_features_target(df_encoded, target_col)

        # 5. 划分训练/测试集
        X_train, X_test, y_train, y_test = self.split_train_test(X, y)

        # 6. 特征缩放（可选）
        if scale:
            X_train_processed, X_test_processed = self.scale_features(X_train, X_test)
        else:
            X_train_processed = self.preprocessor.transform(X_train)
            X_test_processed = self.preprocessor.transform(X_test)

        # 返回完整结果
        return {
            "raw": df_raw,
            "clean": df_clean,
            "X": X,
            "y": y,
            "X_train": X_train_processed,
            "X_test": X_test_processed,
            "y_train": y_train.values,
            "y_test": y_test.values,
            "feature_names": self.categorical_features + self.numeric_features
        }

    def save_processed(self, result: dict, filename: str = "processed_data.npz"):
        """保存预处理后的数据到processed目录"""
        save_path = self.config.DATA_PROCESSED / filename
        np.savez(
            save_path,
            X_train=result["X_train"],
            X_test=result["X_test"],
            y_train=result["y_train"],
            y_test=result["y_test"]
        )
        print(f"✅ 预处理数据已保存到: {save_path}")