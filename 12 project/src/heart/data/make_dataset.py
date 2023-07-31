"""Make dataset"""
# -*- coding: utf-8 -*-
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split


def read_data(dataset_path: str) -> pd.DataFrame:
    """Reading dataset from path"""
    data = pd.read_csv(dataset_path)
    return data

## функция принимает на вход датафрейм и возвращает два датафреймы как тупле треин и тест датафреймы
def split_train_test_data(data: pd.DataFrame,
                          test_size: float,
                          random_state: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split dataset into random train and test subsets"""
    test_data, train_data = train_test_split(data, test_size=test_size, random_state=random_state)
    return test_data, train_data
    