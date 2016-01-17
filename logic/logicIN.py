# -*- coding: UTF-8 -*-
from .logic import LogicPt


class LogicIN(LogicPt):

    def __init__(self):
        super().__init__()
        self.count_input = -1
        self.count_output = 0  # 0-бесконечность
        """Количество входов и выходов."""

        # Hard parametrs
        self.coord_form = tuple()  # Координаты формы полигона
        self.coord_conn = (
            (0.5, 0.5, 0.5, "out"),
        )

        self.name = "in"
        self.writed_name = "in"  # Отображаемое название
        return

    def calc(self, v):
        """
        Функция описывает как обрабатывается входящие значение и подсчитывается результат.
        В каждом логическом элементе своя своя.
        """
        return self.to_bool(v[0])

LogicPt.logicModules["in"] = "LogicIN"
