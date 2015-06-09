import sys
from PyQt4 import QtGui, QtCore
from mcanvas import MCanvas
from mresult import MResult
from mainlogic import MainLogic

class MainWindow(QtGui.QWidget):

    def setWire(self):
        print("wire!")
        self.mcanvas.click_type = "WIRE"

    def setAND(self):
        self.mcanvas.click_type = "AND"

    def setOR(self):
        self.mcanvas.click_type = "OR"

    def setNOT(self):
        print("NOT")
        self.mcanvas.click_type = "NOT"

    def setIN(self):
        self.mcanvas.click_type = "IN"

    def setOUT(self):
        self.mcanvas.click_type = "OUT"

    def saveScheme(self):
        file = open("in.txt", "w")

        for e in self.mcanvas.elements:
            type_elem = e["type"].lower
            if type_elem == "in":
                file.write(e["type"].lower() + ','.join(map(str, e["out"])) + "\n")
            else:
                file.write(e["type"].lower() + " " + ','.join(map(str, e["in"])) + " "
                            + ','.join(map(str, e["out"])) + "\n")

        file.close()

        QtGui.QMessageBox.question(self, 'Message', "Scheme saved", QtGui.QMessageBox.Yes)
        return

    def calc(self):
        self.saveScheme()
        l = MainLogic(self)
        l.fileParser()
        count, values = l.genInputValues()
        self.mresult.setValueTable(values)
        return

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.mcanvas = MCanvas(self)
        self.mcanvas.setMinimumHeight(500)
        self.mcanvas.setMinimumWidth(500)

        self.mresult = MResult(self)

        #self.setGeometry(300, 300, 250, 150)
        #self.resize(250, 150)
        self.setWindowTitle('PyQT LogicScheme Constructor 0.01')

        btnWire = QtGui.QPushButton("Wire")
        self.connect(btnWire, QtCore.SIGNAL('clicked()'), self.setWire)

        btnNo = QtGui.QPushButton("NO")
        self.connect(btnNo, QtCore.SIGNAL('clicked()'), self.setNOT)

        btnOr = QtGui.QPushButton("OR")
        self.connect(btnOr, QtCore.SIGNAL('clicked()'), self.setOR)

        btnAnd = QtGui.QPushButton("AND")
        self.connect(btnAnd, QtCore.SIGNAL('clicked()'), self.setAND)

        btnIn = QtGui.QPushButton("IN")
        self.connect(btnIn, QtCore.SIGNAL('clicked()'), self.setIN)

        btnOut = QtGui.QPushButton("OUT")
        self.connect(btnOut, QtCore.SIGNAL('clicked()'), self.setOUT)

        btnCalc = QtGui.QPushButton("Calc")
        self.connect(btnCalc, QtCore.SIGNAL('clicked()'), self.calc)

        btnSave = QtGui.QPushButton("Save")
        self.connect(btnSave, QtCore.SIGNAL('clicked()'), self.saveScheme)

        btnQuit = QtGui.QPushButton("QUIT", self)
        #self.connect(btnAnd, QtCore.SIGNAL('clicked()'), quit)

        vbox1 = QtGui.QVBoxLayout()
        vbox1.addWidget(btnWire)
        vbox1.addWidget(btnNo)
        vbox1.addWidget(btnOr)
        vbox1.addWidget(btnAnd)
        vbox1.addWidget(btnIn)
        vbox1.addWidget(btnOut)
        vbox1.addStretch(1)
        vbox1.addWidget(btnCalc)
        vbox1.addWidget(btnSave)
        vbox1.addWidget(btnQuit)

        vbox2 = QtGui.QVBoxLayout()
        vbox2.addWidget(self.mcanvas)

        vbox3 = QtGui.QVBoxLayout()
        vbox3.addWidget(self.mresult)

        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)
        hbox.addLayout(vbox3)

        self.setLayout(hbox)
        self.setGeometry(300, 300, 800, 500)

app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
