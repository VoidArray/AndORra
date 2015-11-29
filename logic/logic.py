# -*- coding: UTF-8 -*-
class LogicPt:
    """
    Элемент точка, посылает один сигнал на два и более входа.
    Один вход, бесконечное число выходов.
    """

    logicModules = {"pt": "LogicPt"}
    """
    Общий словарь для логических элементов. Каждый добавляет в него строчку.
    обозначение в файле : Имя класса
    """

    def __init__(self):
        """
        Расстанавливаются начальные значения.
        Они должны отличаться от типа элемента к типу и задаются в этом модуле
        """
        self.count_input = 1
        self.count_output = 0  # 0-бесконечность
        """Количество входов и выходов."""

        """Далее параметры для отображения. Их GUI сам добавит"""
        self.coordX = -1
        self.coordY = -1  # Координаты верхнего левого угла

        self.link = dict()  # используется так: { coord_conn[id] : id element}

        self.id = ""

        """Параметры, которые задаются только вручную:"""
        self.coord_form = list()  # Координаты формы полигона
        self.coord_conn = [
            [0.3, 0.5, 0.25, "in"],
            [0.8, 0.5, 0.25, "out"]
        ]
        """
        self.coord_input = list()
        Только для отрисовки на canvas.
        Координаты мест соединения, относительные, от 0 до 1, умножаются на DELTA.
        self.coord_output.add(list(x, y, radius))
        """
        self.name = "pt"
        self.writed_name = "pt"  # Отображаемое название
        return

    def setValues(self, i, o):
        self.input = i
        self.output = o

    def calc(self, v):
        """
        Функция описывает как обрабатывается входящие значение и подсчитывается результат.
        В каждом логическом элементе своя своя.
        """
        return self.to_bool(v[0])

    @staticmethod
    def to_bool(value):
        """
           Converts 'something' to boolean. Raises exception for invalid formats
               Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
               Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
        """
        if str(value).lower() in ("yes", "y", "true",  "t", "1"): return True
        if str(value).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
        raise Exception('Invalid value for boolean conversion: ' + str(value))
