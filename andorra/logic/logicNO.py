# -*- coding: UTF-8 -*-
from .logic import LogicPt


class LogicNO(LogicPt):

    def __init__(self):
        '''
        Расстанавливаются начальные значения.
        Они должны отличаться от типа элемента к типу и задаются в этом модуле
        '''
        super().__init__()
        self.count_input = 2
        self.count_output = 0  # 0-бесконечность

        # Hard parametrs
        self.coord_form = (  # Координаты формы полигона
            (0, 0.3), (1, 0.3),
            (1, 0.7), (0, 0.7)
        )
        self.coord_conn = (
            (0.1, 0.5, 0.2, 'in'),
            (0.9, 0.5, 0.2, 'out')
        )

        self.name = 'not'
        self.writed_name = 'NOT'  # Отображаемое название
        self.image_file = 'not.png'

    def calc(self, v):
        for k, i in enumerate(v):
            v[k] = not LogicPt.to_bool(i)
        return int(v[0])

LogicPt.logicModules['not'] = 'LogicNO'
