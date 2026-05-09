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
