# -*- coding: UTF-8 -*-
from logicElem import Elem

class LogicNO(Elem):

    def calc(self, v):
        for k, i in enumerate(v):
            v[k] = not Elem.to_bool(i)
        return int(v[0])
