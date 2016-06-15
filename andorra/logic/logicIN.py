# -*- coding: UTF-8 -*-
from .logic import LogicPt


class LogicIN(LogicPt):

    def __init__(self):
        super().__init__()
        self.count_input = -1
        self.count_output = 0  # 0-бесконечность
        '''Количество входов и выходов.'''

        # Hard parametrs
        self.coord_form = (
            (0.3, 0.45), (1, 0.45), (1, 0.55), (0.3, 0.55)
        )  # Координаты формы полигона
        self.coord_conn = (
            (0.9, 0.5, 0.2, 'out'),
        )

        self.name = 'in'
        self.writed_name = 'IN'  # Отображаемое название
        self.image_file = None  # 'in.png'

    def calc(self, v):
        '''
        Функция описывает как обрабатывается входящие значение и подсчитывается результат.
        В каждом логическом элементе своя своя.
        '''
        return self.to_bool(v[0])

LogicPt.logicModules['in'] = 'LogicIN'
