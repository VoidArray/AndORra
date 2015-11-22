from PyQt5 import QtGui, QtWidgets, QtCore

class MResult(QtWidgets.QWidget):

    colCount = 0
    rowCount = 0
    heightCell = 20
    widthCell = 15
    countInput = 0
    countOutput = 0
    table = list()

    def __init__(self, parent):
        super(MResult, self).__init__(parent)
        self.parent = parent

    def setValueTable(self, i, o, val):
        self.table = val
        self.countInput = i
        self.countOutput = o
        self.update()

    def paintEvent(self, e): # событие перерисовки
        qp = QtGui.QPainter()
        qp.begin(self)

        qp.setFont(QtGui.QFont('monotype', 9))
        qp.setPen(QtCore.Qt.black)
        qp.setBrush(QtCore.Qt.black)

        qp.drawText(0, 0, "Таблица истинности")
        for x in range(0, self.countInput):
            qp.drawText(self.widthCell * x, self.heightCell, chr(65 + x))

        qp.drawLine(self.widthCell * self.countInput - self.widthCell / 3, 0,
                    self.widthCell * self.countInput - self.widthCell / 3, self.heightCell * (2 ** self.countInput + 2))

        for x in range(0, self.countOutput):
            qp.drawText(self.widthCell * (x + self.countInput), self.heightCell, chr(65 + x))

        for y, row in enumerate(self.table):
            for x, cell in enumerate(row):
                qp.drawText(self.widthCell * x, self.heightCell * (y + 2), str(cell))

        qp.end()
