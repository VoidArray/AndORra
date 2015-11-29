import random

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint

from logic import *


class MCanvas(QWidget):

    DELTA = 32  # Размеры каждого элемента и радиус при отрисовке

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.clearAll()
        self.setMouseTracking(True)

    def clearAll(self):
        self.wires = list()  # dict from и to - id в elements, coordX1, coordY2
        self.elements = dict()  # словарь всех логических элементов
        """
        dict type, coordX, coordY, in, out, id
        храним координаты ЛЕВОГО ВЕРХНЕГО УГЛА
        и входные - выходные контакты
        """
        self.delta_grag_x = 0
        self.delta_grag_y = 0
        self.draggin_idx = -1  # id выбранного элемента
        self.click_type = ""
        self.selected_connection = dict()
        self.wire_begin = dict()
        self.update()
        self.parent.setStatus("Все детали удалены")
        print("all clear")

    def paintEvent(self, e): # событие перерисовки
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawElements(qp)
        self.drawWires(qp)
        self.drawSelectedConnect(qp)
        qp.end()

    def drawElements(self, qp):  # функция для перерисовки фигур
        count_in = 0
        сount_out = 0
        for t in self.elements:  # Перебираем все элементы
            element = self.elements[t]
            R = self.DELTA / 2
            qp.setFont(QtGui.QFont('monotype', 8))
            qp.setPen(QtCore.Qt.black)
            qp.setBrush(QtCore.Qt.black)
            # Получаем все точки для отрисовки полигона
            polygon_coord = list()
            for c in element.coord_form:
                p = QPoint(element.coordX + c[0] * self.DELTA, element.coordY + c[1] * self.DELTA)
                polygon_coord.append(p)
            # Рисуем форму
            if len(polygon_coord) > 2:
                qp.drawPolygon(QtGui.QPolygon(polygon_coord))
            # Рисуем точки соединений
            qp.setPen(QtCore.Qt.gray)
            qp.setBrush(QtCore.Qt.gray)
            for c in element.coord_conn:
                qp.drawEllipse(element.coordX + c[0] * self.DELTA - c[2] * 4,
                               element.coordY + c[1] * self.DELTA - c[2] * 4,
                               c[2] * R, c[2] * R)
            # Пишем тип элемента
            qp.setPen(QtCore.Qt.red)
            qp.setFont(QtGui.QFont('monotype', 10))
            qp.drawText(element.coordX + c[0], element.coordY + c[1] + self.DELTA, element.writed_name)
            # Буква над входными и выходными элементами
            qp.setPen(QtCore.Qt.black)
            if element.name.upper() == "IN":
                count_in += 1
                qp.drawText(element.coordX, element.coordY - R, chr(64 + count_in))

            if element.name.upper() == "OUT":
                сount_out += 1
                qp.drawText(element.coordX, element.coordY - R, chr(64 + сount_out))
        return

    def drawWires(self, qp):  # функция для перерисовки соединяющих проводов
        qp.setPen(QtCore.Qt.black)
        for t in self.wires:
            qp.drawLine(t["coordX1"], t["coordY1"], t["coordX2"], t["coordY2"])
        return

    def drawSelectedConnect(self, qp):
        if len(self.selected_connection) > 2:
            qp.setPen(QtCore.Qt.yellow)
            qp.setBrush(QtCore.Qt.yellow)
            qp.drawEllipse(self.selected_connection["x"], self.selected_connection["y"],
                    self.selected_connection["r"], self.selected_connection["r"])

    def delConnectByElemId(self, idToDel):
        for w in self.wires:
            if idToDel == w["id1"]:
                id_linked_element = w["id2"]
            elif idToDel == w["id2"]:
                id_linked_element = w["id1"]
            else:
                continue
            if idToDel in (self.elements[id_linked_element]).link:
                (self.elements[id_linked_element]).link_in.remove(idToDel)
            self.wires.remove(w)

    def mousePressEvent(self, evt): #нажатие кнопки мыши
        if evt.button() == QtCore.Qt.RightButton and self.draggin_idx == -1: #правая кнопка мыши - удаляем объект
            for id_key in list(self.elements.keys()):
                element = self.elements[id_key]
                if ((element.coordX < evt.pos().x()) and (element.coordX + self.DELTA * 2 > evt.pos().x()) and
                        (element.coordY < evt.pos().y()) and (element.coordY + self.DELTA * 2 > evt.pos().y())):
                    idToDel = element.id
                    self.delConnectByElemId(idToDel)
                    print("del ", element.name, element.id)
                    self.parent.setStatus("Удален элемент " + element.name)
                    del self.elements[id_key]
                    self.update()

        if self.draggin_idx != -1 and self.click_type == "WIRE" and len(self.selected_connection) > 0: # проверяем можно ли достроить провод
            print("Try WIRE!")
            # Перебор полный не нужен, так как у нас есть значение после event
            if self.wire_begin["type"] != self.selected_connection["type"]:  # соединений между inner - inner не должно быть
                elem2 = self.elements[self.selected_connection["id"]]  # Проверим наличие других связок в этих местах
                if self.selected_connection["num"] in elem2.link:
                    del elem2.link[self.selected_connection["num"]]
                    self.delConnectByElemId(elem2.id)
                    print("ReWrite value at conn")

                elem1 = self.elements[self.wire_begin["id"]]
                if self.wire_begin["num"] in elem1.link:
                    del elem1.link[self.wire_begin["num"]]
                    self.delConnectByElemId(elem1.id)
                    print("ReWrite value at conn")

                self.wires.append({"id2": elem2.id, "id1": elem1.id,
                                   "num2": self.selected_connection["num"],
                                   "num1": self.wire_begin["num"],
                                    "coordX2": elem2.coordX + elem2.coord_conn[self.selected_connection["num"]][0] * self.DELTA,
                                    "coordY2": elem2.coordY + elem2.coord_conn[self.selected_connection["num"]][1] * self.DELTA,
                                    "coordX1": elem1.coordX + elem1.coord_conn[self.wire_begin["num"]][0] * self.DELTA,
                                    "coordY1": elem1.coordY + elem1.coord_conn[self.wire_begin["num"]][1] * self.DELTA
                                   })
                #далее добавляем в элементы
                elem2.link[self.selected_connection["num"]] = elem1.id
                elem1.link[self.wire_begin["num"]] = elem2.id
                #
                self.click_type = ""
                self.draggin_idx = -1
                self.parent.setStatus("Соединение создано")
                print("wire created", self.draggin_idx)
            else:
                self.parent.setStatus("Соединять нужно вход к выходу или наоборот.")

        if evt.button() == QtCore.Qt.LeftButton and self.draggin_idx == -1 and \
                (self.click_type == "" or self.click_type == "WIRE"):  # выделение элемента или начало построения провода
            for i, element in enumerate(self.elements):
                element = self.elements[element]
                if ((element.coordX < evt.pos().x()) and (element.coordX + self.DELTA * 2 > evt.pos().x()) and
                        (element.coordY < evt.pos().y()) and (element.coordY + self.DELTA * 2 > evt.pos().y())):
                    self.draggin_idx = element.id
                    self.delta_grag_x = evt.pos().x() - element.coordX
                    self.delta_grag_y = evt.pos().y() - element.coordY
                    print("drag element id", self.draggin_idx)

                    if (self.click_type == "WIRE") and (len(self.selected_connection) > 2):
                        self.wire_begin["id"] = self.selected_connection["id"]
                        self.wire_begin["type"] = self.selected_connection["type"]
                        self.wire_begin["num"] = self.selected_connection["num"]
                        self.parent.setStatus("Выделите второй элемент")

        if self.click_type != "WIRE" and self.click_type != "":  # Добавление нового элемента
            element = globals()[LogicPt.logicModules[self.click_type.lower()]]()
            element.coordX = evt.pos().x() - self.DELTA / 2
            element.coordY = evt.pos().y() - self.DELTA / 2

            char_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # Генератор id
            element.id = self.click_type + ''.join(random.sample(char_set*6, 6))

            self.elements[element.id] = element
            print("add element", element.name, element.id, len(self.elements))
            self.parent.setStatus("Добавлен элемент " + element.writed_name)
            self.click_type = ""
            self.update()
            return

    def mouseMoveEvent(self, evt):  # Изменение координат во время движения мыши
        if self.draggin_idx != -1 and self.click_type != "WIRE":
            t = self.elements[self.draggin_idx]
            t.coordX = evt.pos().x() - self.delta_grag_x
            t.coordY = evt.pos().y() - self.delta_grag_y
            self.elements[self.draggin_idx] = t
            # Пересчитываем координаты соединений
            for w in self.wires:
                if w["id1"] == self.draggin_idx:
                    conn_coord = t.coord_conn[w["num1"]]
                    w["coordX1"] = t.coordX + conn_coord[0] * self.DELTA
                    w["coordY1"] = t.coordY + conn_coord[1] * self.DELTA
                if w["id2"] == self.draggin_idx:
                    conn_coord = t.coord_conn[w["num2"]]
                    w["coordX2"] = t.coordX + conn_coord[0] * self.DELTA
                    w["coordY2"] = t.coordY + conn_coord[1] * self.DELTA
            self.update()

        # Ищем и выделяем цветом контакт на элементе
        finded = False
        for t in self.elements:
                t = self.elements[t]
                if ((t.coordX < evt.pos().x()) and (t.coordX + self.DELTA * 2 > evt.pos().x()) and
                        (t.coordY < evt.pos().y()) and (t.coordY + self.DELTA * 2 > evt.pos().y())):
                    # Далее как-то перебрать контакты
                    for i, link in enumerate(t.coord_conn):
                        if ((t.coordX + link[0] * self.DELTA - self.DELTA < evt.pos().x())
                                and (t.coordX + link[0] * self.DELTA + self.DELTA > evt.pos().x())
                                and (t.coordY + link[1] * self.DELTA - self.DELTA < evt.pos().y())
                                and (t.coordY + link[1] * self.DELTA + self.DELTA > evt.pos().y())):
                            # Нашли нужное место, далее надо его выделить цветом
                            self.selected_connection = {"x": int(t.coordX + link[0] * self.DELTA),
                                                        "y": int(t.coordY + link[1] * self.DELTA),
                                                        "r": int(link[2] * self.DELTA),
                                                        "type": link[3], "num": i, "id": t.id}
                            finded = True
                            self.update()
                            break
                if finded:
                    break
        if not finded:
            self.selected_connection = dict()

    def mouseReleaseEvent(self, evt): #изменение координат после отпускания кнопки
        if evt.button() == QtCore.Qt.LeftButton and self.draggin_idx != -1 and self.click_type != "WIRE":
            t = self.elements[self.draggin_idx]
            t.coordX = evt.pos().x() - self.delta_grag_x
            t.coordY = evt.pos().y() - self.delta_grag_y
            self.elements[self.draggin_idx] = t
            self.draggin_idx = -1
            self.update()
