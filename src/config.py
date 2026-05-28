from pathlib import Path

class Config:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    DATA_RAW = PROJECT_ROOT / "data" / "raw"
    DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

    OUTPUTS_MODELS = PROJECT_ROOT / "outputs" / "models"
    OUTPUTS_FIGURES = PROJECT_ROOT / "outputs" / "figures"
    OUTPUTS_TABLES = PROJECT_ROOT / "outputs" / "tables"

    RANDOM_SEED = 42
    TEST_SIZE = 0.2
    VAL_SIZE = 0.1

    # ==========================================
    # 网格搜索的超参数空间 (按 README 规范补齐)
    # ==========================================
    # 1. 决策树 / 随机森林
    TREE_PARAMS = {
        'max_depth': [None, 5, 10, 15],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    RF_PARAMS = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5]
    }
    # 2. SVM
    SVM_PARAMS = {
        'C': [0.1, 1, 10],
        'kernel': ['linear', 'rbf']
    }
    # 3. KNN
    KNN_PARAMS = {
        'n_neighbors': [3, 5, 7, 9],
        'weights': ['uniform', 'distance']
    }
    # 4. 岭回归 (Ridge) / Lasso
    RIDGE_LASSO_PARAMS = {
        'alpha': [0.01, 0.1, 1.0, 10.0]
    }