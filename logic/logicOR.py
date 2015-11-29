# -*- coding: UTF-8 -*-
from .logic import LogicPt


class LogicOR(LogicPt):

    def __init__(self):
        """
        Расстанавливаются начальные значения.
        Они должны отличаться от типа элемента к типу и задаются в этом модуле
        """
        super().__init__()
        self.count_input = 2
        self.count_output = 0  # 0-бесконечность

        #Hard parametrs
        self.coord_form = [
            [0, 0], [0.6, 0], [1, 0.5], [0.6, 1], [0, 1]
        ]  # Координаты формы полигона
        self.coord_conn = [
            [0, 0, 0.5, "in"], [0, 1, 0.5, "in"],
            [1, 0.5, 0.5, "out"]
        ]

        self.name = "or"
        self.writed_name = "OR"  # Отображаемое название
        return

    def calc(self, v):
        s = str(v[0])
        for i in v:
            s = LogicPt.to_bool(s) | LogicPt.to_bool(i)
        return int(s)

LogicPt.logicModules["or"] = "LogicOR"

