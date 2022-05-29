import os
import csv
import pathlib
import pandas as pd
from enum import Enum


data_dir = os.path.join(pathlib.Path(__file__).parent.parent, 'data')


class Dataset(Enum):
    Fruithut = 0
    Liquor = 1


def load_dataframe(filename):
    filepath = os.path.join(os.path.dirname(__file__), data_dir, filename)
    dataframe = pd.read_csv(filepath, header=None)
    return dataframe


def load_list(filename):
    filepath = os.path.join(os.path.dirname(__file__), data_dir, filename)
    all_items = []
    transactions = []
    with open(filepath, newline='') as f:
        for line in f:
            transaction = line.split()
            all_items.extend(transaction)
            transactions.append(transaction)
    unique_items = list(set(all_items))
    return transactions, unique_items


def display_files():
    for dirname, _, filenames in os.walk(data_dir):
        filenames = filter(lambda fname: fname.endswith('.txt'), filenames)
        for filename in filenames:
            print(os.path.join(dirname, filename))


def load_dataset(dataset: Dataset):
    if dataset == Dataset(0):
        transactions = load_list('fruithut/fruithut_original.txt')
        taxonomy = load_dataframe('fruithut/taxonomy.txt')
    elif dataset == Dataset(1):
        transactions = load_list('liquor/liquor_11frequent.txt')
        taxonomy = load_dataframe('liquor/taxonomy.txt')
    else:
        transactions, taxonomy = None, None

    return transactions, taxonomy
