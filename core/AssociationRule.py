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
        conf_percent = int(100*self._conf)
        return f'{p} -> {s} (sup={self._sup},conf={conf_percent}%)'

    def csv_format(self) -> str:
        pred = ','.join(map(str, self._pred))
        suc = ','.join(map(str, self._suc))
        sup_str = str(self._sup)
        conf_str = f'{self._conf:.4f}'
        csv = ';'.join([pred, suc, sup_str, conf_str]) + '\n'
        return csv
