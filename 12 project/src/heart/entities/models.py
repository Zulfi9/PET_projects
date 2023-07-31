"""Models contains Random Forest and Logistic regression models"""
from typing import Any #, Optional
from dataclasses import dataclass, field


@dataclass
class RFConfig:
    """Class for Random Forest """
    #pass
    # алгоритм Random Forest, название и все значения дефолтов из файла конфиг,
    # и все прописываем по аналогии с логистической регрессией, которая была написана.
    # Расставляем типы данных
    _target_: str = field(default='sklearn.ensemble.RandomForestClassifier')
    max_depth: int = field(default=3)
    n_estimators: int = field(default=100)
    random_state: int = field(default=42)


@dataclass
class LogregConfig:
    """Class for  Logistic regression models"""
    _target_: str = field(default='sklearn.linear_model.LogisticRegression')
    penalty: str = field(default='l1')
    solver: str = field(default='liblinear')
    C: float = field(default=1.0)
    random_state: int = field(default=42)
    max_iter: int = field(default=100)


@dataclass
class ModelConfig:
    """Class for  model_name and model_params types"""
    model_name: str
    model_params: Any
