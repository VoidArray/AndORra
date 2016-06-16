import random
import math

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint

from andorra.logic import *


class MCanvas(QWidget):
    DELTA = 64  # Размеры каждого элемента и диаметр при отрисовке

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

    def paintEvent(self, e):  # событие перерисовки
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawElements(qp)
        self.drawWires(qp)
        self.drawSelectedConnect(qp)
        qp.end()

    def drawElements(self, qp):  # функция для перерисовки фигур
        count_in = 0
        сount_out = 0
        for element_id in self.elements:  # Перебираем все элементы
            element = self.elements[element_id]
            R = self.DELTA / 2
            qp.setPen(QtCore.Qt.black)
            qp.setBrush(QtCore.Qt.black)
            if hasattr(element, 'image_file') and element.image_file:
                # Рисуем иконку
                image_name = 'img/' + element.image_file
                element_image = QtGui.QPixmap(image_name)
                element_image = element_image.scaled(self.DELTA, self.DELTA, QtCore.Qt.KeepAspectRatio)
                qp.drawPixmap(element.coordX, element.coordY, element_image)
            else:
                # Получаем все точки для отрисовки формы в виде полигона
                if len(element.coord_form) > 2:
                    polygon_coord = list()
                    for c in element.coord_form:
                        p = QPoint(element.coordX + c[0] * self.DELTA, element.coordY + c[1] * self.DELTA)
                        polygon_coord.append(p)
                    # Рисуем форму
                    if len(polygon_coord) > 2:
                        qp.drawPolygon(QtGui.QPolygon(polygon_coord))
            # Рисуем точки соединений
            qp.setPen(QtCore.Qt.black)
            qp.setBrush(QtCore.Qt.black)
            for c in element.coord_conn:
                qp.drawEllipse(QPoint(int(element.coordX + c[0] * self.DELTA),
                                      int(element.coordY + c[1] * self.DELTA)),
                               int(c[2] * R), int(c[2] * R))
            # Пишем тип элемента
            qp.setPen(QtCore.Qt.red)
            qp.setFont(QtGui.QFont('monotype', 10))
            qp.drawText(element.coordX + c[0], element.coordY + c[1] + self.DELTA, element.writed_name)
            # Буква над входными и выходными элементами
            qp.setPen(QtCore.Qt.black)
            if element.name.upper() == "IN":
                count_in += 1
                qp.drawText(element.coordX, element.coordY, chr(64 + count_in))

            if element.name.upper() == "OUT":
                сount_out += 1
                qp.drawText(element.coordX, element.coordY, chr(64 + сount_out))

    def drawWires(self, qp):  # функция для перерисовки соединяющих проводов
        blackPen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(blackPen)
        for t in self.wires:
            # qp.drawLine(t["coordX1"], t["coordY1"], t["coordX2"], t["coordY2"])
            qp.drawLine(t["coordX1"], t["coordY1"], t["coordX1"], t["coordY2"])
            qp.drawLine(t["coordX1"], t["coordY2"], t["coordX2"], t["coordY2"])

    def drawSelectedConnect(self, qp):
        if len(self.selected_connection) > 2:
            qp.setPen(QtCore.Qt.yellow)
            qp.setBrush(QtCore.Qt.yellow)
            qp.drawEllipse(QPoint(self.selected_connection["x"], self.selected_connection["y"]),
                           self.selected_connection["r"], self.selected_connection["r"])

        if len(self.wire_begin) > 2:
            qp.setPen(QtCore.Qt.yellow)
            qp.setBrush(QtCore.Qt.red)
            qp.drawEllipse(QPoint(self.wire_begin["x"], self.wire_begin["y"]),
                           self.wire_begin["r"], self.wire_begin["r"])

    def delAllWireByElemId(self, idToDel):
        for w in list(self.wires):
            if idToDel == w["id1"]:
                id_linked_element = w["id2"]
                numConnect = w["num2"]
            elif idToDel == w["id2"]:
                id_linked_element = w["id1"]
                numConnect = w["num1"]
            else:
                continue
            if idToDel in list((self.elements[id_linked_element]).link[numConnect]):
                ((self.elements[id_linked_element]).link[numConnect]).remove(idToDel)
            self.wires.remove(w)

    def delOneWire(self, id1, id2):
        assert type(id1) is str and type(id2) is str
        for w in self.wires:
            if id1 == w["id1"] and id2 == w["id2"] or id1 == w["id2"] and id2 == w["id1"]:
                self.wires.remove(w)

    def mousePressEvent(self, evt):  # нажатие кнопки мыши
        if evt.button() == QtCore.Qt.RightButton and self.draggin_idx == -1:  # правая кнопка мыши - удаляем объект
            isElementDeleted = False
            for id_key in list(self.elements.keys()):
                element = self.elements[id_key]
                if ((element.coordX < evt.pos().x()) and (element.coordX + self.DELTA > evt.pos().x()) and
                        (element.coordY < evt.pos().y()) and (element.coordY + self.DELTA > evt.pos().y())):
                    idToDel = element.id
                    self.delAllWireByElemId(idToDel)
                    print("del ", element.name, element.id)
                    self.parent.setStatus("Удален элемент " + element.name)
                    del self.elements[id_key]
                    self.update()
                    isElementDeleted = True
            print('elem to del not found')
            if not isElementDeleted:  # Не был найден подходящий элемент, ищем провод для удаления
                distance = list()
                for w in self.wires:
                    d = math.fabs(  # Находим расстояние между каждым проводом и координатами клика
                        ((w["coordY2"] - w["coordY1"]) * evt.pos().x() + (w["coordX1"] - w["coordX2"]) * evt.pos().y() +
                        (w["coordX2"] * w["coordY1"] - w["coordX1"] * w["coordY2"])) /
                        math.sqrt(math.pow(w["coordX1"] - w["coordX2"], 2) + math.pow(w["coordY1"] - w["coordY2"], 2))
                    )
                    distance.append(d)
                # Далее находим самый близкий провод
                min_distance = distance[0]
                min_idx = 0
                for i, d in enumerate(distance):
                    if d < min_distance:
                        min_distance = d
                        min_idx = i
                # Удаляем провод если расстояние меньше DELTA
                if min_distance < self.DELTA:
                    w = self.wires[min_idx]
                    print("min distance: ", min_distance, min_idx, w["id1"], w["id2"], )
                    element_1 = self.elements[w["id1"]]
                    element_1_list = element_1.link[w["num1"]]
                    if w["id2"] in element_1_list:
                        element_1_list.remove(w["id2"])

                    element_2 = self.elements[w["id2"]]
                    element_2_list = element_1.link[w["num2"]]
                    if w["id1"] in element_2_list:
                        element_2_list.remove(w["id1"])

                    # (self.elements[w["id1"]].link[w["num1"]]).remove(w["id2"])
                    # (self.elements[w["id2"]].link[w["num2"]]).remove(w["id1"])
                    self.wires.remove(w)

        if self.draggin_idx != -1 and self.click_type == "WIRE" and len(self.selected_connection) > 0:
            # проверяем можно ли достроить провод
            print("Try WIRE!")
            # Перебор полный не нужен, так как у нас есть значение selected_connection
            if self.wire_begin["type"] != self.selected_connection["type"]:  # соединений между inner - inner не должно быть
                # Проверяем наличие других связок в этих местах
                print("Type true")
                elem1 = self.elements[self.wire_begin["id"]]
                elem2 = self.elements[self.selected_connection["id"]]
                if elem1.id != elem2.id:
                    if self.selected_connection["num"] in elem2.link:
                        if self.selected_connection["type"] != "out":  # исходящих может быть любое количество
                            self.delOneWire(elem2.id, elem2.link[self.selected_connection["num"]][0])
                            print("ReWrite value at conn")
                            elem2.link[self.selected_connection["num"]] = list()
                        (elem2.link[self.selected_connection["num"]]).append(elem1.id)
                    else:
                        elem2.link[self.selected_connection["num"]] = [elem1.id, ]
                    print('count check')
                    if self.wire_begin["num"] in elem1.link:
                        if self.wire_begin["type"] != "out":  # исходящих может быть любое количество
                            self.delOneWire(elem1.id, elem1.link[self.wire_begin["num"]][0])
                            print("ReWrite value at conn")
                            elem1.link[self.wire_begin["num"]] = list()
                        (elem1.link[self.wire_begin["num"]]).append(elem2.id)
                    else:
                        elem1.link[self.wire_begin["num"]] = [elem2.id, ]
                    print('count check 2')
                    self.wires.append({"id2": elem2.id, "id1": elem1.id,
                                       "num2": self.selected_connection["num"],
                                       "num1": self.wire_begin["num"],
                                       "coordX2": elem2.coordX + elem2.coord_conn[self.selected_connection["num"]][
                                                                     0] * self.DELTA,
                                       "coordY2": elem2.coordY + elem2.coord_conn[self.selected_connection["num"]][
                                                                     1] * self.DELTA,
                                       "coordX1": elem1.coordX + elem1.coord_conn[self.wire_begin["num"]][0] * self.DELTA,
                                       "coordY1": elem1.coordY + elem1.coord_conn[self.wire_begin["num"]][1] * self.DELTA
                                       })
                    #
                    self.click_type = ""
                    self.draggin_idx = -1
                    self.parent.setStatus("Соединение создано")
                    self.wire_begin.clear()
                    print("wire created", self.draggin_idx)
                else:
                    self.parent.setStatus("Соединять необходимо два разных элемента")
            else:
                self.parent.setStatus("Соединять необходимо вход к выходу или наоборот.")

        if evt.button() == QtCore.Qt.LeftButton and self.draggin_idx == -1 and \
                (self.click_type == "" or self.click_type == "WIRE"):  # выделение элемента или начало построения провода
            for i, element in enumerate(self.elements):
                element = self.elements[element]
                if ((element.coordX < evt.pos().x()) and (element.coordX + self.DELTA > evt.pos().x()) and
                        (element.coordY < evt.pos().y()) and (element.coordY + self.DELTA > evt.pos().y())):
                    self.draggin_idx = element.id
                    self.delta_grag_x = evt.pos().x() - element.coordX
                    self.delta_grag_y = evt.pos().y() - element.coordY
                    print("drag element id", self.draggin_idx)

                    if (self.click_type == "WIRE") and (len(self.selected_connection) > 2):
                        self.wire_begin = dict(self.selected_connection)
                        self.parent.setStatus("Выделите второй элемент")

        if self.click_type != "WIRE" and self.click_type != "":  # Добавление нового элемента
            element_type = LogicPt.logicModules[self.click_type.lower()]
            element = globals()[element_type]()
            element.coordX = evt.pos().x() - self.DELTA / 2
            element.coordY = evt.pos().y() - self.DELTA / 2

            char_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # Генератор id
            element.id = self.click_type + ''.join(random.sample(char_set * 6, 6))

            self.elements[element.id] = element
            print("add element", element.name, element.id, len(self.elements))
            self.parent.setStatus("Добавлен элемент " + element.writed_name)
            self.click_type = ""
            self.update()

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

        # Ищем и выделяем цветом контакт на элементе
        finded = False
        for t in self.elements:
            t = self.elements[t]
            if ((t.coordX < evt.pos().x()) and (t.coordX + self.DELTA > evt.pos().x()) and
                    (t.coordY < evt.pos().y()) and (t.coordY + self.DELTA > evt.pos().y())):
                # Далее как-то перебрать контакты
                for i, link in enumerate(t.coord_conn):
                    if ((t.coordX + link[0] * self.DELTA - link[2] * self.DELTA < evt.pos().x())
                        and (t.coordX + link[0] * self.DELTA + link[2] * self.DELTA > evt.pos().x())
                        and (t.coordY + link[1] * self.DELTA - link[2] * self.DELTA < evt.pos().y())
                        and (t.coordY + link[1] * self.DELTA + link[2] * self.DELTA > evt.pos().y())):
                        # Нашли нужное место, далее надо его выделить цветом
                        self.selected_connection = {"x": int(t.coordX + link[0] * self.DELTA),
                                                    "y": int(t.coordY + link[1] * self.DELTA),
                                                    "r": int(link[2] * self.DELTA / 3),
                                                    "type": link[3], "num": i, "id": t.id}
                        finded = True
                        break
            if finded:
                break
        if not finded:
            self.selected_connection.clear()

        self.update()

    def mouseReleaseEvent(self, evt):  # изменение координат после отпускания кнопки
        if evt.button() == QtCore.Qt.LeftButton and self.draggin_idx != -1 and self.click_type != "WIRE":
            coordX = evt.pos().x() if evt.pos().x() >= 0 else 0
            coordY = evt.pos().y() if evt.pos().y() >= 0 else 0
            t = self.elements[self.draggin_idx]
            t.coordX = coordX - self.delta_grag_x
            t.coordY = coordY - self.delta_grag_y
            self.draggin_idx = -1
            self.update()
