"""Build feutures """
from typing import List

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler


def process_categorical_features(categorical_df: pd.DataFrame) -> pd.DataFrame:
    """Function returns categorical pipeline to df """
    categorical_pipeline = build_categorical_pipeline()
    return pd.DataFrame(categorical_pipeline.fit_transform(categorical_df).toarray())


def build_categorical_pipeline() -> Pipeline:
    """Function returns categorical pipeline"""
    categorical_pipeline = Pipeline(
        [
            # ADD SimpleImputer for Categorical Preprocessing добавили импутер
            ("imputer", SimpleImputer(strategy='most_frequent')),
            ("ohe", OneHotEncoder()),
        ]
    )
    return categorical_pipeline


def process_numerical_features(numerical_df: pd.DataFrame) -> pd.DataFrame:
    """Function returns numerical pipeline to df """
    num_pipeline = build_numerical_pipeline()
    return pd.DataFrame(num_pipeline.fit_transform(numerical_df))


def build_numerical_pipeline() -> Pipeline:
    """Function returns numerical pipeline"""
    num_pipeline = Pipeline(
        [
            # Add Transforms добавили outlier_remover и scaler
            ('outlier_remover', OutlierRemover()),
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())

        ]
    )
    return num_pipeline


def make_features(transformer: ColumnTransformer, df: pd.DataFrame) -> pd.DataFrame:
    """Function returns transformed df """
    return pd.DataFrame(transformer.transform(df))


def extract_target(df: pd.DataFrame, target_col: List[str]) -> pd.Series:
    """Function returns target """
    target = df[target_col].values
    return target


class OutlierRemover(BaseEstimator, TransformerMixin):
    """OutlierRemover class """
    def __init__(self, factor=1.5):
        """self.factor """
        self.factor = factor

    def outlier_removal(self, x: pd.DataFrame):
        """returns pd.series """
        x = pd.Series(x).copy()
        q1 = x.quantile(0.25)
        q3 = x.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - (self.factor * iqr)
        upper_bound = q3 + (self.factor * iqr)
        x.loc[((x < lower_bound) | (x > upper_bound))] = np.nan
        return pd.Series(x)

    def fit(self, x, y=None):
        """returns sef"""
        return self

    def transform(self, x: np.array):
        """pd.DataFrame"""
        return pd.DataFrame(x).apply(self.outlier_removal)


def build_transformer(categorical_features: List[str],
                      numerical_features: List[str]) -> ColumnTransformer:
    """returns transformer"""
    transformer = ColumnTransformer(
        [
            (
                "categorical_pipeline",
                build_categorical_pipeline(),
                #[c for c in categorical_features],
                list(categorical_features)
            ),
            (
        # Numerical feature Pipeline добавили numerical_pipeline
                "numerical_pipeline",
                build_numerical_pipeline(),
                list(numerical_features)
            )
        ]
    )
    return transformer
