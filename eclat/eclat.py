from utils.load_data import display_files, load_dataset, Dataset


def run_eclat():
    transactions, taxonomy = load_dataset(Dataset(0))
    print(transactions, taxonomy)


def mine_frequent_itemsets():
    pass
