import os
import random
import numpy as np


def set_seed(seed: int = 42):
    """
    统一设置所有常用的随机种子，保证模型训练的可复现性。
    无论你在哪里跑，结果都是一样的！
    """
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)

    # 如果你们之后有人要用 PyTorch，这段也会很有用
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass


def ensure_dir(path) -> None:
    """
    确保目录存在（递归创建）。被 Preprocessor/Trainer/Evaluator 等共享使用。
    放在 utils 里避免各处重复 mkdir(parents=True, exist_ok=True)。
    C 负责维护此工具函数。
    """
    from pathlib import Path
    Path(path).mkdir(parents=True, exist_ok=True)
