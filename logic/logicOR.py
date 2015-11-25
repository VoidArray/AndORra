# -*- coding: UTF-8 -*-
from .logic import LogicPt


class LogicOR(LogicPt):

    LogicPt.logicModules["or"] = "LogicOR"

    def calc(self, v):
        s = str(v[0])
        for i in v:
            s = LogicPt.to_bool(s) | LogicPt.to_bool(i)
        return int(s)

