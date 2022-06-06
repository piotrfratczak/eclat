class AssociationRule:
    def __init__(self, pred: frozenset, suc: frozenset, sup: int, conf: float):
        self.pred = pred
        self.suc = suc
        self.sup = sup
        self.conf = conf

    def __str__(self):
        p = set(self.pred)
        s = set(self.suc)
        return f'{p} -> {s}'
