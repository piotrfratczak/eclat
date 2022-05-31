import pandas as pd

from utils.load_data import display_files, load_dataset, Dataset


def run_eclat():
    transactions, taxonomy = load_dataset(Dataset(0))
    dummies = get_dummies(transactions)


def mine_frequent_itemsets():
    pass


def get_dummies(transactions):
    return pd.get_dummies(transactions.stack()).groupby(level=0).max()
