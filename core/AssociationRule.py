class AssociationRule:
    def __init__(self, pred: tuple, suc: tuple, sup: int, conf: float):
        self._pred = pred
        self._suc = suc
        self._sup = sup
        self._conf = conf

    def __eq__(self, other):
        if isinstance(other, AssociationRule):
            return self._pred == other._pred and self._suc == other._suc
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __str__(self):
        p = set(self._pred)
        s = set(self._suc)
        return f'{p} -> {s} (conf={self._conf:.2f})'
