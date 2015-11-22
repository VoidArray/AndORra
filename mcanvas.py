from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint

class MCanvas(QWidget):

    DELTA = 16 #for the minimum distance
    click_type = ""

    elements = list()
    #dict type, coordX, coordY, in, out
    #храним координаты ЛЕВОГО ВЕРХНЕГО УГЛА
    #и входные - выходные контакты
    wires = list()
    #dict from и to - индексы в elements
    wiresCount = 0

    def __init__(self, parent):
        super(MCanvas, self).__init__(parent)
        self.clearAll()

        self.parent = parent

    def clearAll(self):
        self.wires = list()
        self.wiresCount = 0
        self.elements = list()
        self.draggin_idx = -1 #индекс двигаемого элемента
        self.click_type = ""
        self.update()
        print("all clear")

    def paintEvent(self, e): # событие перерисовки
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawElements(qp)
        self.drawWires(qp)
        qp.end()

    def drawElements(self, qp): # функция для перерисовки фигур
        inCounter = 0
        outCounter = 0
        #qp.setPen(QtCore.Qt.black)
        for t in self.elements:
            #qp.setBrush(QtGui.QColor(25, 0, 90, 200))
            R = self.DELTA / 2
            qp.setFont(QtGui.QFont('monotype', 8))
            writedType = ""

            if t["type"] == "IN":
                qp.setPen(QtCore.Qt.black)
                qp.setBrush(QtCore.Qt.black)
                qp.drawEllipse(t["coordX"], t["coordY"] + R, self.DELTA, self.DELTA)
                qp.drawRect(t["coordX"] + self.DELTA, t["coordY"] + self.DELTA, self.DELTA, R/2)
                inCounter += 1
                qp.drawText(t["coordX"], t["coordY"] - R, chr(64 + inCounter))
                writedType = "IN"

            if t["type"] == "OUT":
                qp.setPen(QtCore.Qt.black)
                qp.setBrush(QtCore.Qt.black)
                qp.drawRect(t["coordX"], t["coordY"] + R, self.DELTA, self.DELTA)
                qp.drawLine(t["coordX"], t["coordY"], t["coordX"] + self.DELTA * 2, t["coordY"] + self.DELTA) #рисуем стрелку
                qp.drawLine(t["coordX"], t["coordY"] + self.DELTA * 2, t["coordX"] + self.DELTA * 2, t["coordY"] + self.DELTA)
                outCounter += 1
                qp.drawText(t["coordX"], t["coordY"] - R, chr(64 + outCounter))
                writedType = "OUT"

            if t["type"] == "OR" or t["type"] == "AND": # общее
                qp.setPen(QtCore.Qt.darkCyan)
                qp.setBrush(QtCore.Qt.black)

                qp.drawPolygon(QPoint(t["coordX"], t["coordY"]),
                               QPoint(t["coordX"] + self.DELTA, t["coordY"]),
                               QPoint(t["coordX"] + self.DELTA * 2, t["coordY"] + self.DELTA),
                               QPoint(t["coordX"] + self.DELTA, t["coordY"] + self.DELTA * 2),
                               QPoint(t["coordX"], t["coordY"] + self.DELTA * 2)
                               )

                qp.drawEllipse(t["coordX"] - R / 2, t["coordY"] - R/2, R, R) #три строчки контактов
                qp.drawEllipse(t["coordX"] - R / 2, t["coordY"] + self.DELTA * 2 - R/2, R, R)
                qp.drawEllipse(t["coordX"] + self.DELTA * 2 - R/2, t["coordY"] + self.DELTA - R/2, R, R)

            if t["type"] == "OR":
                writedType = "\/"

            if t["type"] == "AND":
                writedType = "/\\"

            if t["type"] == "NOT":
                qp.setPen(QtCore.Qt.darkCyan)
                qp.setBrush(QtCore.Qt.black)

                qp.drawRect(t["coordX"], t["coordY"] +R , self.DELTA * 2, self.DELTA)

                qp.drawEllipse(t["coordX"] - R / 2, t["coordY"] + self.DELTA - R/2, R, R)
                qp.drawEllipse(t["coordX"] + self.DELTA * 2 - R/2, t["coordY"] + self.DELTA - R/2, R, R)
                writedType = "¬"

            qp.setPen(QtCore.Qt.red) #пишем тип элемента
            qp.setFont(QtGui.QFont('monotype', 10))
            qp.drawText(t["coordX"] + R, t["coordY"] + self.DELTA, writedType)

    def drawWires(self, qp): # функция для перерисовки соединяющих проводов
        qp.setPen(QtCore.Qt.black)
        for i, t in enumerate(self.wires):
            p1 = self.elements[t["from"]]
            p2 = self.elements[t["to"]]
            #p1 вывод, значит всегда вывод по центру рисуется #найдем к какому месту рисовать вход
            if (len(p2["in"]) == 1): #один вход - посередине
                qp.drawLine(p1["coordX"] + self.DELTA * 2, p1["coordY"] + self.DELTA, p2["coordX"], p2["coordY"] + self.DELTA)
            elif i+1 in (p2["in"])[1:]: #второй вывод - левый нижний угол
                qp.drawLine(p1["coordX"] + self.DELTA * 2, p1["coordY"] + self.DELTA, p2["coordX"], p2["coordY"] + self.DELTA * 2)
            else:
                qp.drawLine(p1["coordX"] + self.DELTA * 2, p1["coordY"] + self.DELTA, p2["coordX"], p2["coordY"])
        return

    def mousePressEvent(self, evt): #нажатие кнопки мыши
        if evt.button() == QtCore.Qt.RightButton and self.draggin_idx == -1: #правая кнопка мыши - удаляем объект
            for i, t in enumerate(self.elements):
                if ((t["coordX"] < evt.pos().x()) and (t["coordX"] + self.DELTA * 2 > evt.pos().x()) and
                        (t["coordY"] < evt.pos().y()) and (t["coordY"] + self.DELTA * 2 > evt.pos().y())):
                        for w in self.wires:
                            if i == w["from"] or i == w["to"]:
                                self.wires.remove(w)
                                if i == w["from"]:
                                    (self.elements[w["to"]])["in"].remove(i)
                                if i == w["to"]:
                                    (self.elements[w["from"]])["out"].remove(i)
                        self.elements.remove(t)
                        self.update()

        if self.draggin_idx != -1 and self.click_type == "WIRE": #проверяем можно ли достроить провод
            for i, t in enumerate(self.elements):
                if ((t["coordX"] < evt.pos().x()) and (t["coordX"] + self.DELTA * 2 > evt.pos().x()) and
                        (t["coordY"] < evt.pos().y()) and (t["coordY"] + self.DELTA * 2 > evt.pos().y())):
                    self.wires.append({"from": self.draggin_idx, "to": i})
                    self.wiresCount += 1
                    #далее добавляем в элементы
                    ((self.elements[i])["in"]).append(self.wiresCount)
                    ((self.elements[self.draggin_idx])["out"]).append(self.wiresCount)
                    #
                    self.click_type = ""
                    self.draggin_idx = -1
                    self.parent.setStatus("Wire created")
                    print("wire created", self.draggin_idx)

        if evt.button() == QtCore.Qt.LeftButton and self.draggin_idx == -1 and \
                (self.click_type == "" or self.click_type == "WIRE"):
            for i, t in enumerate(self.elements):
                if ((t["coordX"] < evt.pos().x() ) and (t["coordX"] + self.DELTA * 2 > evt.pos().x()) and
                        (t["coordY"] < evt.pos().y() ) and (t["coordY"] + self.DELTA * 2 > evt.pos().y())):
                    self.draggin_idx = i
                    print("drag element id", self.draggin_idx)

                    if self.click_type == "WIRE":
                        self.parent.setStatus("Выделите второй элемент")

        if self.click_type != "WIRE" and self.click_type != "": #Добавление элемента
            e = dict()
            e["coordX"] = evt.pos().x() - self.DELTA
            e["coordY"] = evt.pos().y() - self.DELTA
            e["type"] = self.click_type
            e["in"] = list()
            e["out"] = list()
            self.click_type = ""
            self.elements.append(e)
            print("add element", e["type"], len(self.elements))
            self.parent.setStatus("Добавлен элемент")
            self.update()
            return

    def mouseMoveEvent(self, evt): # Изменение координат во время движения
        if self.draggin_idx != -1 and self.click_type != "WIRE":
            t = self.elements[self.draggin_idx]
            t["coordX"] = evt.pos().x() - self.DELTA
            t["coordY"] = evt.pos().y() - self.DELTA
            self.elements[self.draggin_idx] = t
            self.update()

    def mouseReleaseEvent(self, evt): #изменение координат после отпускания кнопки
        if evt.button() == QtCore.Qt.LeftButton and self.draggin_idx != -1 and self.click_type != "WIRE":
            t = self.elements[self.draggin_idx]
            t["coordX"] = evt.pos().x() - self.DELTA
            t["coordY"] = evt.pos().y() - self.DELTA
            self.elements[self.draggin_idx] = t
            self.draggin_idx = -1
            self.update()
