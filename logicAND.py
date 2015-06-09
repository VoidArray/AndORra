# -*- coding: UTF-8 -*-
from logicElem import Elem

class LogicAND(Elem):

    def calc(self, v):
        s = v[0]
        for i in v:
            s = Elem.to_bool(s) & Elem.to_bool(i)
        return int(s)
