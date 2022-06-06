import time
import pandas as pd
from itertools import combinations

from core.AssociationRule import AssociationRule


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


def rule_gen(frequent: list[list[tuple]], sup_dict: dict, min_conf: float, min_len: int, max_len: int = None) ->\
        list[AssociationRule]:
    if min_conf < 0.0 or min_conf > 1.0:
        raise ValueError(f'Parameter min_conf should be in [0, 1] but {min_conf} was passed.')
    if max_len is not None and min_len > max_len:
        raise ValueError(f'Parameter min_len should be less than max_len but min_len: {min_len} and max_len: {max_len}')
    if min_len > len(frequent):
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


def find_hierarchy(tax_dict: dict, ancestor_dict: dict, item: int) -> tuple[set, dict]:
    """
    Find all ancestors of item in hierarchy.
    """
    if item in ancestor_dict:
        return ancestor_dict[item], ancestor_dict

    ancestors = set()
    parent = item
    while parent in tax_dict:
        parent = tax_dict[parent]
        ancestors.add(parent)
    ancestor_dict.update({item: ancestors})
    return ancestors, ancestor_dict


def hierarchy_rule(frequent: list[list[tuple]], tax_dict: dict, sup_dict: dict) -> list[AssociationRule]:
    """
    Mine special rules based on taxonomy.

    Generate special rules a -> Ah such that a is an element in a transaction
    and Ah is an element in hierarchy that a belongs to. If there are transactions
    {a, b} where a and b belong to Ah.

    :param frequent: List L of lists li of tuples that represent itemsets sorted by their length
        (the first element of list L - l1 - stores itemsets of length 1,
        the next element of L - l2 - stores itemsets of length 2 and so on).
    :param tax_dict: Hierarchy dictionary of elements in frequent {child: parent}.
    :param sup_dict: Dictionary of supports for each itemset.
    :return: List of the special rules described above.
    """
    if len(frequent) < 2:
        return []
    rules = set()
    ancestor_dict = {}
    two_itemsets = frequent[1]
    for itemset in two_itemsets:
        item1 = itemset[0]
        item2 = itemset[1]
        ancestors1, ancestor_dict = find_hierarchy(tax_dict, ancestor_dict, item1)
        ancestors2, ancestor_dict = find_hierarchy(tax_dict, ancestor_dict, item2)
        common = ancestors1.intersection(ancestors2)
        for h_item in common:
            ar1 = AssociationRule((item1,), (h_item,), sup_dict[(item1,)], 1.0)
            rules.add(ar1)
            ar2 = AssociationRule((item2,), (h_item,), sup_dict[(item2,)], 1.0)
            rules.add(ar2)

    rules = list(rules)
    return rules


def eclat(transactions: pd.DataFrame, taxonomy: pd.DataFrame = None, min_sup: int = 1, min_conf: float = 0.5,
          min_len: int = 1, max_len: int = None) -> list[AssociationRule]:
    print('\nStart ECLAT.')
    start_time = time.time()

    frequent, sup_dict = frequent_itemsets(transactions, min_sup)
    frequent_time = time.time()
    print(f'\nFrequent itemsets mined - number of frequent itemsets: {len(sup_dict.keys())}.'
          f'\nCompleted in {frequent_time-start_time:.4f} sec.')

    rules = rule_gen(frequent, sup_dict, min_conf, min_len, max_len)
    rules_time = time.time()
    print(f'\nAssociation rules mined - number of frequent rules: {len(rules)}.'
          f'\nCompleted in {rules_time-frequent_time:.4f} sec.')

    if taxonomy is not None:
        tax_dict = taxonomy.set_index('child')['parent'].to_dict()
        h_rules = hierarchy_rule(frequent, tax_dict, sup_dict)
        rules.extend(h_rules)
        hierarchy_time = time.time()
        print(f'\nHierarchy rules mined - total number of rules: {len(rules)}.'
              f'\nCompleted in {hierarchy_time-rules_time:.4f} sec.')

    return rules
