import sys
import pickle

from PyQt5.QtWidgets import *
from mcanvas import MCanvas
from mresult import MResult
from mainlogic import MainLogic

class MainWindow(QWidget):

    def setElement(self):
        self.mcanvas.click_type = self.sender().toolTip

    def clearScheme(self):
        self.mcanvas.clearAll()

    def openFileDialog(self):
        file_name = QFileDialog.getOpenFileName()
        print("load from", file_name[0])
        self.loadScheme(file_name[0])

    def loadScheme(self, fileName): #загрузка графической схемы
        f = open(fileName, "rb")
        self.mcanvas.elements = pickle.load(f)
        self.mcanvas.wires = pickle.load(f)
        f.close()
        self.setStatus("Схема загружена" + fileName)
        return

    def saveFileDialog(self):
        file_name = QFileDialog.getSaveFileName()
        print("Save to", file_name[0])
        self.saveScheme(file_name[0])

    def saveScheme(self, fileName): #сохранение графической схемы
        f = open(fileName, "wb")
        pickle.dump(self.mcanvas.elements, f)
        pickle.dump(self.mcanvas.wires, f)
        f.close()
        self.setStatus("Схема сохранена в файл " + fileName)
        return

    def saveLogic(self):
        file = open("in.txt", "w")

        for t in self.mcanvas.elements:
            e = self.mcanvas.elements[t]
            input_id = list()
            output_id = list()

            if len(e.link) < len(e.coord_conn):  # не все входы-выходы заполнены у элемента
                print("wrong connection", e.id)
                continue

            for j, w in enumerate(self.mcanvas.wires):
                if w["id1"] == e.id:
                    num = w["num1"]
                elif w["id2"] == e.id:
                    num = w["num2"]
                else:
                    continue
                if e.coord_conn[num][3] == "in":
                    input_id.append(j)
                else:
                    output_id.append(j)

            if e.name.lower == "in":
                file.write(e.name.lower() + " " + e.id + ','.join(map(str, output_id)) + "\n")
            else:
                file.write(e.name.lower() + " " + e.id + " " + ','.join(map(str, input_id)) + " " +
                           ','.join(map(str, output_id)) + "\n")

        file.close()
        self.setStatus("Logic saved")
        return

    def calc(self):
        self.saveLogic()
        l = MainLogic(self)
        l.fileParser()
        countInputs, countOutputs, values = l.genInputValues()
        self.mresult.setValueTable(countInputs, countOutputs, values)
        return

    def setStatus(self, status):
        mainwin.statusBar().showMessage(status)

    def __init__(self):
        super().__init__()

        self.setMinimumHeight(500)
        self.setMinimumWidth(800)
        self.mcanvas = MCanvas(self)
        self.mcanvas.setMinimumHeight(500)
        self.mcanvas.setMinimumWidth(500)

        self.mresult = MResult(self)
        self.mresult.width = 100

        btnWire = QPushButton("Соединить")
        btnWire.toolTip = "WIRE"
        btnWire.clicked.connect(self.setElement)

        btnPt = QPushButton("PT")
        btnPt.toolTip = "PT"
        btnPt.clicked.connect(self.setElement)

        btnNo = QPushButton("NOT")
        btnNo.toolTip = "NOT"
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

        btnCalc = QPushButton("Подсчитать")
        btnCalc.clicked.connect(self.calc)

        btnSaveScheme = QPushButton("Сохранить в файл")
        btnSaveScheme.clicked.connect(self.saveFileDialog)

        btnLoadScheme = QPushButton("Загрузить файл")
        btnLoadScheme.clicked.connect(self.openFileDialog)

        btnSave = QPushButton("Save")
        btnSave.clicked.connect(self.saveLogic)

        btnQuit = QPushButton("QUIT", self)
        btnQuit.clicked.connect(quit)

        btnClear = QPushButton("Clear", self)
        btnClear.clicked.connect(self.clearScheme)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(btnWire)
        vbox1.addWidget(btnPt)
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

        hbox = QGridLayout()
        hbox.addLayout(vbox1, 0, 0)
        hbox.addLayout(vbox2, 0, 1, 1, 6)
        hbox.addLayout(vbox3, 0, 7)

        self.setLayout(hbox)
        self.resize(800, 500)
        self.setStatus("Ready to work")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwin = QMainWindow()
    mainwin.setWindowTitle('AndORra - конструктор логических схем')
    main = MainWindow()
    main.loadScheme("123.el")
    mainwin.setCentralWidget(main)
    mainwin.show()
    st = app.exec_()
    print("exit")
    sys.exit(st)

