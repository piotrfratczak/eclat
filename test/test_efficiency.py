import time
import argparse
import pandas as pd

from core.eclat import eclat
from utils.data_io import Dataset, load_predefined, save_test


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=11)
    parser.add_argument('--vertical', type=int, default=28)
    parser.add_argument('--horizontal', type=int, default=16)
    parser.add_argument('--hierarchy', type=int, default=10000)
    args = parser.parse_args()
    print(args)
    return args


def vertical_test(test_range: int, n: int) -> None:
    results = {'n_rules': [], 'time': []}
    transactions0, taxonomy = load_predefined(Dataset(-1))
    for i in range(n):
        transactions = transactions0.copy()
        for p in range(test_range):
            transactions = pd.concat([transactions, transactions], ignore_index=True)
            start_time = time.time()
            eclat(transactions, taxonomy=None, min_sup=0, min_conf=0.0, min_len=1)
            results['n_rules'].append(pow(2, p))
            results['time'].append(time.time() - start_time)

    results_df = pd.DataFrame(results)
    save_test(results_df, 'vertical')
    results_agg = results_df.groupby("n_rules")["time"].agg({'mean', 'std', 'min', 'max'})
    save_test(results_agg, 'vertical_agg')

    print('-' * 20)
    print(f'\nVertical test completed.')


def horizontal_test(test_range: int, n: int) -> None:
    results = {'n_items': [], 'time': []}
    for i in range(n):
        transactions = {0: 10 * [0]}
        for columns in range(1, test_range):
            transactions.update({columns: 10 * [columns]})
            transactions_df = pd.DataFrame(transactions)
            start_time = time.time()
            eclat(transactions_df, taxonomy=None, min_sup=0, min_conf=0.0, min_len=1)
            results['n_items'].append(columns)
            results['time'].append(time.time() - start_time)

    results_df = pd.DataFrame(results)
    save_test(results_df, 'horizontal')
    results_agg = results_df.groupby("n_items")["time"].agg({'mean', 'std', 'min', 'max'})
    save_test(results_agg, 'horizontal_agg')

    print('-' * 20)
    print(f'\nHorizontal test completed.')


def hierarchy_test(test_range: int, n: int) -> None:
    results = {'n_hierarchy': [], 'time': []}
    transactions, _ = load_predefined(Dataset(-1))
    for i in range(n):
        children = [1, 2]
        parents = [3, 3]
        for e in range(3, test_range):
            taxonomy = {'child': children, 'parent': parents}
            taxonomy_df = pd.DataFrame(taxonomy)
            start_time = time.time()
            eclat(transactions, taxonomy=taxonomy_df, min_sup=0, min_conf=0.0, min_len=1)
            results['time'].append(time.time() - start_time)
            results['n_hierarchy'].append(e-1)
            children.append(e)
            parents.append(e+1)

    results_df = pd.DataFrame(results)
    save_test(results_df, 'hierarchy')
    results_agg = results_df.groupby("n_hierarchy")["time"].agg({'mean', 'std', 'min', 'max'})
    save_test(results_agg, 'hierarchy_agg')

    print('-' * 20)
    print(f'\nHierarchy test completed.')


if __name__ == "__main__":
    args = parse_args()
    hierarchy_test(args.hierarchy, args.n)
    horizontal_test(args.horizontal, args.n)
    vertical_test(args.vertical, args.n)
