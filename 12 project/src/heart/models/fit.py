"""It is s fit.py module"""
import pickle
from typing import Union

import pandas as pd
from hydra.utils import instantiate
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


SklearnRegressionModel = Union[RandomForestClassifier, LogisticRegression]


def train_model(
    model_params, train_features: pd.DataFrame, target: pd.Series
) -> SklearnRegressionModel:
    """Function returns model"""
    model = instantiate(model_params).fit(train_features, target.ravel())
    return model


def serialize_model(model: SklearnRegressionModel, output: str) -> str:
    """Function returns output"""
    with open(output, "wb") as f: # pylint: disable=C0103
        pickle.dump(model, f)
    return output
