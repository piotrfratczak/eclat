import io
import pandas as pd
from unittest import TestCase

from core.eclat import get_tidlists, frequent_itemsets, rule_gen, hierarchy_rule, eclat
from core.AssociationRule import AssociationRule


class TestEclat(TestCase):

    def test_tidlists(self):
        s = '1 2\n' \
            '1 2\n' \
            '1 3'
        file = io.StringIO(s)
        transactions = pd.read_csv(file, index_col=None, sep=' ', names=range(2))
        tid_dict, sup_dict = get_tidlists(transactions, 1)

        expected_tid = {(1,): frozenset({0, 1, 2}), (2,): frozenset({0, 1})}
        self.assertEqual(tid_dict, expected_tid)
        expected_sup = {(1,): 3, (2,): 2}
        self.assertEqual(sup_dict, expected_sup)

    def test_frequent(self):
        s = '1 2\n' \
            '1 2\n' \
            '1 3'
        file = io.StringIO(s)
        transactions = pd.read_csv(file, index_col=None, sep=' ', names=range(2))
        frequent, sup_dict = frequent_itemsets(transactions, min_sup=1)

        expected_frequent = [[(1,), (2,)], [(1, 2)]]
        self.assertEqual(frequent, expected_frequent)
        expected_sup = {(1,): 3, (2,): 2, (1, 2): 2}
        self.assertEqual(sup_dict, expected_sup)

    def test_rule_gen(self):
        s = '1 2\n' \
            '1 2\n' \
            '1 3'
        file = io.StringIO(s)
        transactions = pd.read_csv(file, index_col=None, sep=' ', names=range(2))
        frequent, sup_dict = frequent_itemsets(transactions, min_sup=1)
        rules = rule_gen(frequent, sup_dict, min_conf=0.1, min_len=1)

        expected1 = AssociationRule((1,), (2,), 2, 2/3)
        expected2 = AssociationRule((2,), (1,), 2, 2/2)
        self.assertEqual(set(rules), {expected1, expected2})

    def test_rule_gen2(self):
        s = '1 2\n' \
            '1 2\n' \
            '1 3'
        file = io.StringIO(s)
        transactions = pd.read_csv(file, index_col=None, sep=' ', names=range(2))
        frequent, sup_dict = frequent_itemsets(transactions, min_sup=1)
        rules = rule_gen(frequent, sup_dict, min_conf=0.9, min_len=1)  # <- min_conf=0.9

        expected = AssociationRule((2,), (1,), 2, 2/2)
        self.assertEqual(set(rules), {expected})

    def test_hierarchy_rule(self):
        s = '1 2\n' \
            '1 2\n' \
            '1 3'
        t = '1,11\n' \
            '2,11\n' \
            '3,33\n' \
            '11,22'
        file = io.StringIO(s)
        tax_file = io.StringIO(t)
        transactions = pd.read_csv(file, index_col=None, sep=' ', names=range(2))
        taxonomy = pd.read_csv(tax_file, sep=',', header=None, names=['child', 'parent'])
        frequent, sup_dict = frequent_itemsets(transactions, min_sup=1)
        tax_dict = taxonomy.set_index('child')['parent'].to_dict()
        h_rules = hierarchy_rule(frequent, tax_dict, sup_dict)

        expected1 = AssociationRule((1,), (11,), 3, 3/3)
        expected2 = AssociationRule((2,), (11,), 2, 2/2)
        expected3 = AssociationRule((1,), (22,), 3, 3/3)
        expected4 = AssociationRule((2,), (22,), 2, 2/2)
        self.assertEqual(set(h_rules), {expected1, expected2, expected3, expected4})

    def test_hierarchy_rule2(self):
        s = '1 2\n' \
            '1 2\n' \
            '1 3'
        t = '1,11\n' \
            '2,11\n' \
            '3,33\n' \
            '11,22\n' \
            '33,22'
        file = io.StringIO(s)
        tax_file = io.StringIO(t)
        transactions = pd.read_csv(file, index_col=None, sep=' ', names=range(2))
        taxonomy = pd.read_csv(tax_file, sep=',', header=None, names=['child', 'parent'])
        frequent, sup_dict = frequent_itemsets(transactions, min_sup=0)  # <- min_sup=0
        tax_dict = taxonomy.set_index('child')['parent'].to_dict()
        h_rules = hierarchy_rule(frequent, tax_dict, sup_dict)

        expected1 = AssociationRule((1,), (11,), 3, 3/3)
        expected2 = AssociationRule((2,), (11,), 2, 2/2)
        expected3 = AssociationRule((1,), (22,), 3, 3/3)
        expected4 = AssociationRule((2,), (22,), 2, 2/2)
        expected5 = AssociationRule((3,), (22,), 1, 1/1)
        self.assertEqual(set(h_rules), {expected1, expected2, expected3, expected4, expected5})

    def test_eclat(self):
        s = '1 2\n' \
            '1 2\n' \
            '1 2 3\n' \
            '2 3'
        t = '1,11\n' \
            '2,11\n' \
            '3,33\n' \
            '11,22'
        file = io.StringIO(s)
        tax_file = io.StringIO(t)
        transactions = pd.read_csv(file, index_col=None, sep=' ', names=range(3))
        taxonomy = pd.read_csv(tax_file, sep=',', header=None, names=['child', 'parent'])
        rules = eclat(transactions, taxonomy, min_sup=2, min_conf=0.7, min_len=1)

        expected1 = AssociationRule((1,), (2,), 3, 3/3)
        expected2 = AssociationRule((2,), (1,), 3, 3/4)
        expected3 = AssociationRule((1,), (11,), 3, 3/3)
        expected4 = AssociationRule((2,), (11,), 4, 4/4)
        expected5 = AssociationRule((1,), (22,), 3, 3/3)
        expected6 = AssociationRule((2,), (22,), 4, 4/4)
        self.assertEqual(set(rules), {expected1, expected2, expected3, expected4, expected5, expected6})
