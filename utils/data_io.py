import os
import time
import pathlib
import pandas as pd
from enum import Enum

from core.AssociationRule import AssociationRule


data_dir = os.path.join(pathlib.Path(__file__).parent.parent, 'data')
output_dir = os.path.join(pathlib.Path(__file__).parent.parent, 'output')


class Dataset(Enum):
    Test = -1
    Debug = 0
    Fruithut = 1
    Liquor = 2


def load_predefined(dataset: Dataset) -> tuple[pd.DataFrame, pd.DataFrame]:
    if dataset == Dataset.Test:
        filepath = os.path.join(data_dir, 'test/test.txt')
        tax_filepath = os.path.join(data_dir, 'test/taxonomy.txt')
    elif dataset == Dataset.Debug:
        filepath = os.path.join(data_dir, 'debug/taxonomy.txt')
        tax_filepath = os.path.join(data_dir, 'debug/taxonomy.txt')
    elif dataset == Dataset.Fruithut:
        filepath = os.path.join(data_dir, 'fruithut/fruithut_original.txt')
        tax_filepath = os.path.join(data_dir, 'fruithut/taxonomy.txt')
    elif dataset == Dataset.Liquor:
        filepath = os.path.join(data_dir, 'liquor/liquor_11frequent.txt')
        tax_filepath = os.path.join(data_dir, 'liquor/taxonomy.txt')
    else:
        raise ValueError(f'Dataset "{dataset}" not found.')

    transactions, taxonomy = load_dataset(filepath, tax_filepath)
    return transactions, taxonomy


def load_dataset(filepath: str, taxonomy_path: str = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    start_time = time.time()
    transactions = load_dataframe(filepath)
    taxonomy = None
    if taxonomy_path:
        taxonomy = load_dataframe(taxonomy_path, is_taxonomy=True)
    print(f'\nDataset loaded - number of transactions: {len(transactions.index)}.'
          f'\nCompleted in {time.time()-start_time:.4f} sec.')
    return transactions, taxonomy


def load_dataframe(filepath: str, is_taxonomy: bool = False) -> pd.DataFrame:
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


def save_rules(rules: list[AssociationRule], filename: str = f'results_{time.strftime("%Y%m%d-%H%M%S")}.csv'):
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        f.write(';'.join(['predecessor', 'successor', 'support', 'confidence']) + '\n')
        for rule in rules:
            f.writelines(rule.csv_format())


def save_test(result: pd.DataFrame, test_type: str):
    filename = f'test_{test_type}_{time.strftime("%Y%m%d-%H%M%S")}.csv'
    filepath = os.path.join(output_dir, filename)
    result.to_csv(filepath)
