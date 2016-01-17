# -*- coding: UTF-8 -*-
from .logic import LogicPt


class LogicNO(LogicPt):

    def __init__(self):
        """
        Расстанавливаются начальные значения.
        Они должны отличаться от типа элемента к типу и задаются в этом модуле
        """
        super().__init__()
        self.count_input = 2
        self.count_output = 0  # 0-бесконечность

        # Hard parametrs
        self.coord_form = (  # Координаты формы полигона
            (0, 0.3), (1, 0.3),
            (1, 0.7), (0, 0.7)
        )
        self.coord_conn = (
            (0, 0.5, 0.5, "in"),
            (1, 0.5, 0.5, "out")
        )

        self.name = "no"
        self.writed_name = "NOT"  # Отображаемое название
        return

    def calc(self, v):
        for k, i in enumerate(v):
            v[k] = not LogicPt.to_bool(i)
        return int(v[0])

LogicPt.logicModules["not"] = "LogicNO"
