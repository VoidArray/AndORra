import sys

from PyQt5.QtWidgets import *
from mcanvas import MCanvas
from mresult import MResult
from mainlogic import MainLogic

class MainWindow(QWidget):

    def setElement(self):
        self.mcanvas.click_type = self.sender().toolTip

    def clearScheme(self):
        self.mcanvas.clearAll()

    def loadScheme(self): #сохранение графической схемы
        file = open("scheme.txt", "r")
        elements = True
        while(f in file):
            pass

        file.close()

        QMessageBox.information(self, 'Message', "Scheme loaded", QMessageBox.Yes)
        return

    def saveScheme(self): #сохранение графической схемы
        file = open("scheme.txt", "w")

        for e in self.mcanvas.elements:
            type_elem = e["type"].lower
            if type_elem == "in":
                file.write(e["type"].lower() + " " + e["coordX"] + " " + e["coordY"] + " " +
                           ','.join(map(str, e["out"])) + "\n")
            else:
                file.write(e["type"].lower() + " " + e["coordX"] + " " + e["coordY"] + " " +
                           ','.join(map(str, e["in"])) + " " + ','.join(map(str, e["out"])) + "\n")

        file.write("wires")
        for w in self.mcanvas.wires:
            file.write(w["from"] + " " + w["to"])

        file.close()

        QMessageBox.information(self, 'Message', "Scheme saved", QMessageBox.Yes)
        return

    def saveLogic(self):
        file = open("in.txt", "w")

        for e in self.mcanvas.elements:
            type_elem = e["type"].lower
            if type_elem == "in":
                file.write(e["type"].lower() + ','.join(map(str, e["out"])) + "\n")
            else:
                file.write(e["type"].lower() + " " + ','.join(map(str, e["in"])) + " "
                            + ','.join(map(str, e["out"])) + "\n")

        file.close()

        QMessageBox.question(self,'Message', "Logic saved", QMessageBox.Yes)
        return

    def calc(self):
        self.saveLogic()
        l = MainLogic(self)
        l.fileParser()
        countInputs, countOutputs, values = l.genInputValues()
        self.mresult.setValueTable(countInputs, countOutputs, values)
        return

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.mcanvas = MCanvas(self)
        self.mcanvas.setMinimumHeight(500)
        self.mcanvas.setMinimumWidth(500)
        self.setWindowTitle('AndORra - конструктор логических схем')

        self.mresult = MResult(self)

        btnWire = QPushButton("Wire")
        btnWire.toolTip = "WIRE"
        btnWire.clicked.connect(self.setElement)

        btnNo = QPushButton("NO")
        btnNo.toolTip = "NO"
        btnNo.clicked.connect(self.setElement)

        btnOr = QPushButton("OR")
        btnOr.toolTip = "OR"
        btnOr.clicked.connect(self.setElement)

        btnAnd = QPushButton("AND")
        btnAnd.toolTip = "AND"
        btnAnd.clicked.connect(self.setElement)

        btnIn = QPushButton("IN")
        btnIn.toolTip = "IN"
        btnIn.clicked.connect(self.setElement)

        btnOut = QPushButton("OUT")
        btnOut.toolTip = "OUT"
        btnOut.clicked.connect(self.setElement)

        btnCalc = QPushButton("Calc")
        btnCalc.clicked.connect(self.calc)

        btnSaveScheme = QPushButton("Сохранить в файл")
        btnSaveScheme.clicked.connect(self.saveScheme)

        btnLoadScheme = QPushButton("Загрузить файл")
        btnLoadScheme.clicked.connect(self.loadScheme)

        btnSave = QPushButton("Save")
        btnSave.clicked.connect(self.saveLogic)

        btnQuit = QPushButton("QUIT", self)
        btnQuit.clicked.connect(quit)

        btnClear = QPushButton("Clear", self)
        btnClear.clicked.connect(self.clearScheme)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(btnWire)
        vbox1.addWidget(btnNo)
        vbox1.addWidget(btnOr)
        vbox1.addWidget(btnAnd)
        vbox1.addWidget(btnIn)
        vbox1.addWidget(btnOut)
        vbox1.addStretch(1)
        vbox1.addWidget(btnCalc)
        vbox1.addWidget(btnLoadScheme)
        vbox1.addWidget(btnSaveScheme)
        vbox1.addWidget(btnSave)
        vbox1.addWidget(btnQuit)
        vbox1.addWidget(btnClear)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.mcanvas)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.mresult)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)
        hbox.addLayout(vbox3)

        self.setLayout(hbox)
        self.resize(800, 500)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
