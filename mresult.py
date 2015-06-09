from PyQt4 import QtGui, QtCore

class MResult(QtGui.QWidget):

    colCount = 0
    rowCount = 0
    heightCell = 15
    widthCell = 15
    table = list()

    def __init__(self, parent):
        super(MResult, self).__init__(parent)
        self.parent = parent

    def setValueTable(self, val):
        self.table = val
        self.update()

    def paintEvent(self, e): # событие перерисовки
        qp = QtGui.QPainter()
        qp.begin(self)

        print("table:", self.table)
        qp.setFont(QtGui.QFont('monotype', 6))
        qp.setPen(QtCore.Qt.red)
        qp.setBrush(QtCore.Qt.yellow)

        qp.drawText(0, 0, "Таблица истинности")

        for y, row in enumerate(self.table):
            for x, cell in enumerate(row):
                qp.drawText(self.widthCell * x, self.heightCell * (y + 1), str(cell))

        qp.end()
