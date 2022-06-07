import time
import argparse

from core.eclat import eclat
from utils.data_io import Dataset, load_predefined, load_dataset, save_rules


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=int, default='0')
    parser.add_argument('--data', type=str)
    parser.add_argument('--taxonomy', type=str)
    args = parser.parse_args()
    print(args)
    return args


def main() -> None:
    args = parse_args()
    if args.data:
        transactions, taxonomy = load_dataset(args.data, args.taxonomy)
    else:
        transactions, taxonomy = load_predefined(Dataset(args.dataset))
    rules = eclat(transactions, taxonomy=taxonomy)
    save_rules(rules)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f'\nTotal execution time: {time.time() - start_time:.4f} sec.')
