import pandas as pd
from itertools import combinations

from core.AssociationRule import AssociationRule
from utils.load_data import load_dataset, Dataset


def get_dummies(transactions: pd.DataFrame) -> pd.DataFrame:
    return pd.get_dummies(transactions.stack()).groupby(level=0).max()


def get_tidlists(transactions: pd.DataFrame, min_sup: int) -> tuple[dict, dict]:
    dummies = get_dummies(transactions)
    dummies = dummies.loc[:, (dummies.sum(axis=0) > min_sup)]
    tid_dict = dict()
    sup_dict = dict()
    for item in dummies.columns:
        tidlist = frozenset(dummies.index[dummies[item] == 1].tolist())
        key = (int(item),)
        tid_dict.update({key: tidlist})
        sup_dict.update({key: len(tidlist)})
    return tid_dict, sup_dict


def frequent_itemsets(transactions: pd.DataFrame, min_sup: int) -> tuple[list[list[tuple]], dict]:
    if min_sup >= len(transactions.index):
        return [], {}

    tid_dict, sup_dict = get_tidlists(transactions, min_sup)
    row = list(tid_dict.keys())
    if len(row) == 0:
        return [], {}

    frequent = [row]
    for _ in range(len(row)):
        prev_row = row
        row = []
        for i1, itemset1 in enumerate(prev_row):
            tidlist1 = tid_dict[itemset1]
            for i2 in range(i1+1, len(prev_row)):
                itemset2 = prev_row[i2]
                if not (itemset1[:-1] == itemset2[:-1] and itemset1[-1] != itemset2[-1]):
                    break
                tidlist2 = tid_dict[itemset2]
                tidlist = tidlist1.intersection(tidlist2)
                if len(tidlist) > min_sup:
                    new_itemset = itemset1 + (itemset2[-1],)
                    row.append(new_itemset)
                    tid_dict.update({new_itemset: tidlist})
                    sup_dict.update({new_itemset: len(tidlist)})
        if len(row) == 0:
            break
        frequent.append(row)

    return frequent, sup_dict


def rule_gen(frequent: list[list[tuple]], sup_dict: dict, min_sup: int, min_conf: float, min_len: int,
             max_len: int = None) -> list[AssociationRule]:
    if min_conf < 0.0 or min_conf > 1.0:
        raise ValueError(f'Parameter min_conf should be in [0, 1] but {min_conf} was passed.')
    if max_len is not None and min_len > max_len:
        raise ValueError(f'Parameter min_len should be less than max_len but min_len: {min_len} and max_len: {max_len}')
    if min_len > len(frequent):
        return []
    if min_sup > sup_dict[frequent[-1][-1]]:
        return []
    if max_len is None:
        max_len = len(frequent)

    rules = []
    for length in range(min_len-1, max_len):
        for itemset in frequent[length]:
            for suc_len in range(1, len(itemset)):
                for suc in combinations(itemset, suc_len):
                    pred = tuple(sorted(set(itemset).difference(suc)))
                    if pred not in sup_dict or suc not in sup_dict:
                        continue
                    sup = sup_dict[itemset]
                    pred_sup = sup_dict[pred]
                    conf = sup/pred_sup
                    if conf <= min_conf:
                        continue
                    ar = AssociationRule(pred, suc, sup, conf)
                    rules.append(ar)
    return rules


def eclat(min_sup: int = 1, min_conf: float = 0.5, min_len: int = 2, max_len: int = None) -> list[AssociationRule]:
    transactions, taxonomy = load_dataset(Dataset(0))
    print('Dataset loaded.')
    frequent, sup_dict = frequent_itemsets(transactions, min_sup)
    print('Frequent itemsets mined.')
    rules = rule_gen(frequent, sup_dict, min_sup, min_conf, min_len, max_len)
    print('Association rules mined.')

    return rules
