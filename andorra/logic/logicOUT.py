# -*- coding: UTF-8 -*-
from .logic import LogicPt


class LogicOUT(LogicPt):

    def __init__(self):
        '''
        Расстанавливаются начальные значения.
        Они должны отличаться от типа элемента к типу и задаются в этом модуле
        '''
        super().__init__()
        self.count_input = 0
        self.count_output = -1  # 0-бесконечность
        '''Количество входов и выходов.'''

        # Hard parametrs
        self.coord_form = (
            (0, 0.45), (0.6, 0.45), (0.6, 0.55), (0, 0.55)
        )  # Координаты формы полигона
        self.coord_conn = (
            (0.1, 0.5, 0.2, 'in'),
        )

        self.name = 'out'
        self.writed_name = 'OUT'  # Отображаемое название
        self.image_file = None  # 'out.png'

    def calc(self, v):
        '''
        Функция описывает как обрабатывается входящие значение и подсчитывается результат.
        В каждом логическом элементе своя своя.
        '''
        return self.to_bool(v[0])

LogicPt.logicModules['out'] = 'LogicOUT'
