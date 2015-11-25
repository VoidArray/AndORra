# -*- coding: UTF-8 -*-
from .logic import LogicPt


class LogicAND(LogicPt):

    LogicPt.logicModules["and"] = "LogicAND"

    def calc(self, v):
        s = v[0]
        for i in v:
            s = LogicPt.to_bool(s) & LogicPt.to_bool(i)
        return int(s)
