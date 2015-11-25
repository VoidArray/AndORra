# -*- coding: UTF-8 -*-
from .logic import LogicPt


class LogicNO(LogicPt):

    LogicPt.logicModules["no"] = "LogicNO"

    def calc(self, v):
        for k, i in enumerate(v):
            v[k] = not LogicPt.to_bool(i)
        return int(v[0])
