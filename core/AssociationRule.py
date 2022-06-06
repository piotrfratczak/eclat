class AssociationRule:
    def __init__(self, pred: tuple, suc: tuple, sup: int, conf: float):
        self.pred = pred
        self.suc = suc
        self.sup = sup
        self.conf = conf

    def __str__(self):
        p = set(self.pred)
        s = set(self.suc)
        return f'{p} -> {s} (conf={self.conf:.2f})'
