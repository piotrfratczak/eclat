import os
import pathlib
import pandas as pd
from enum import Enum


data_dir = os.path.join(pathlib.Path(__file__).parent.parent, 'data')


class Dataset(Enum):
    Debug = 0
    Fruithut = 1
    Liquor = 2


def load_dataset(dataset: Dataset) -> tuple[pd.DataFrame, pd.DataFrame]:
    if dataset == Dataset.Debug:
        transactions = load_dataframe('debug/debug.txt')
        taxonomy = load_dataframe('debug/taxonomy.txt', is_taxonomy=True)
    elif dataset == Dataset.Fruithut:
        transactions = load_dataframe('fruithut/fruithut_original.txt')
        taxonomy = load_dataframe('fruithut/taxonomy.txt', is_taxonomy=True)
    elif dataset == Dataset.Liquor:
        transactions = load_dataframe('liquor/liquor_11frequent.txt')
        taxonomy = load_dataframe('liquor/taxonomy.txt', is_taxonomy=True)
    else:
        raise ValueError(f'Dataset "{dataset}" not found.')

    return transactions, taxonomy


def load_dataframe(filename: str, is_taxonomy: bool = False) -> pd.DataFrame:
    filepath = os.path.join(os.path.dirname(__file__), data_dir, filename)
    if is_taxonomy:
        names = ['child', 'parent']
        separator = ','
    else:
        names = range(find_longest(filepath))
        separator = ' '
    dataframe = pd.read_csv(filepath, sep=separator, header=None, names=names)
    return dataframe


def find_longest(filepath: str) -> int:
    max_len = 0
    with open(filepath, newline='') as f:
        for line in f:
            transaction = line.split()
            max_len = max(max_len, len(transaction))
    return max_len


def display_files() -> None:
    for dirname, _, filenames in os.walk(data_dir):
        filenames = filter(lambda fname: fname.endswith('.txt'), filenames)
        for filename in filenames:
            print(os.path.join(dirname, filename))
