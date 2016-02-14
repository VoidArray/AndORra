import sys
import pickle

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
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
        print('load from', file_name[0])
        self.loadScheme(file_name[0])

    def loadScheme(self, fileName): #загрузка графической схемы
        f = open(fileName, 'rb')
        self.mcanvas.elements = pickle.load(f)
        self.mcanvas.wires = pickle.load(f)
        f.close()
        self.setStatus('Схема загружена' + fileName)
        return

    def saveFileDialog(self):
        file_name = QFileDialog.getSaveFileName()
        print('Save to', file_name[0])
        self.saveScheme(file_name[0])

    def saveScheme(self, fileName): #сохранение графической схемы
        f = open(fileName, 'wb')
        pickle.dump(self.mcanvas.elements, f)
        pickle.dump(self.mcanvas.wires, f)
        f.close()
        self.setStatus('Схема сохранена в файл ' + fileName)
        return

    def saveLogic(self):
        file = open('in.txt', 'w')

        for t in self.mcanvas.elements:
            e = self.mcanvas.elements[t]
            input_id = list()
            output_id = list()

            if len(e.link) < len(e.coord_conn):  # не все входы-выходы заполнены у элемента
                print('wrong connection', e.id)
                continue

            for j, w in enumerate(self.mcanvas.wires):
                if w['id1'] == e.id:
                    num = w['num1']
                elif w['id2'] == e.id:
                    num = w['num2']
                else:
                    continue
                if e.coord_conn[num][3] == 'in':
                    input_id.append(j)
                else:
                    output_id.append(j)

            if e.name.lower == 'in':
                file.write(e.name.lower() + ' ' + e.id + ','.join(map(str, output_id)) + '\n')
            else:
                file.write(e.name.lower() + ' ' + e.id + ' ' + ','.join(map(str, input_id)) + ' ' +
                           ','.join(map(str, output_id)) + '\n')

        file.close()
        self.setStatus('Logic saved')
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

    def __init__(self, menubar):
        super().__init__()

        self.setMinimumHeight(500)
        self.setMinimumWidth(800)
        self.mcanvas = MCanvas(self)
        self.mcanvas.setMinimumHeight(500)
        self.mcanvas.setMinimumWidth(500)

        self.mresult = MResult(self)
        self.mresult.width = 100
        self.menubar = menubar

        # init menu
        actionWire = QAction(QIcon('img/wire.png'), 'Wire', self)
        actionWire.setShortcut('w')
        actionWire.setStatusTip('Connect elements')
        actionWire.toolTip = 'WIRE'
        actionWire.triggered.connect(self.setElement)

        actionPt = QAction(QIcon('img/point.png'), 'Ppint', self)
        actionPt.setShortcut('p')
        actionPt.toolTip = 'PT'
        actionPt.triggered.connect(self.setElement)

        actionNo = QAction(QIcon('img/no.png'), 'NOT', self)
        actionNo.toolTip = 'NOT'
        actionNo.setShortcut('n')
        actionNo.triggered.connect(self.setElement)

        actionOr = QAction(QIcon('img/or.png'), 'OR', self)
        actionOr.toolTip = 'OR'
        actionOr.setShortcut('r')
        actionOr.triggered.connect(self.setElement)

        actionAnd = QAction(QIcon('img/and.png'), 'AND', self)
        actionAnd.toolTip = 'AND'
        actionAnd.setShortcut('a')
        actionAnd.triggered.connect(self.setElement)

        actionIn = QAction(QIcon('img/in.png'), 'IN', self)
        actionIn.toolTip = 'IN'
        actionIn.setShortcut('i')
        actionIn.triggered.connect(self.setElement)

        actionOut = QAction(QIcon('img/in.png'), 'OUT', self)
        actionOut.toolTip = 'OUT'
        actionOut.setShortcut('e')
        actionOut.triggered.connect(self.setElement)

        actionCalc = QAction(QIcon('img/point.png'), 'Подсчитать', self)
        actionCalc.setShortcut('ctrl+c')
        actionCalc.triggered.connect(self.calc)

        actionSaveScheme = QAction(QIcon('img/point.png'), 'Сохранить в файл', self)
        actionSaveScheme.setShortcut('ctrl+s')
        actionSaveScheme.triggered.connect(self.saveFileDialog)

        actionLoadScheme = QAction(QIcon('img/point.png'), 'Загрузить файл', self)
        actionLoadScheme.setShortcut('ctrl+o')
        actionLoadScheme.triggered.connect(self.openFileDialog)

        # actionSave = QPushButton('Save')
        # actionSave.setShortcut('ctrl+s')
        # actionSave.triggered.connect(self.saveLogic)

        actionQuit = QAction(QIcon('img/point.png'), 'QUIT', self)
        actionQuit.setShortcut('ctrl+q')
        actionQuit.triggered.connect(quit)

        actionClear = QAction(QIcon('img/point.png'), 'Clear', self)
        actionClear.setShortcut('del')
        actionClear.triggered.connect(self.clearScheme)

        schemeMenu = self.menubar.addMenu('&Схема')
        schemeMenu.addAction(actionCalc)
        schemeMenu.addAction(actionSaveScheme)
        schemeMenu.addAction(actionLoadScheme)
        schemeMenu.addAction(actionQuit)

        elemMenu = self.menubar.addMenu('&Элементы')
        elemMenu.addAction(actionWire)
        elemMenu.addAction(actionIn)
        elemMenu.addAction(actionOut)
        elemMenu.addAction(actionOr)
        elemMenu.addAction(actionAnd)
        elemMenu.addAction(actionPt)
        # simple buttons
        btnWire = QPushButton(QIcon('img/wire.png'), 'Соединить')
        btnWire.toolTip = 'WIRE'
        btnWire.clicked.connect(self.setElement)

        btnPt = QPushButton(QIcon('img/point.png'), 'PT')
        btnPt.toolTip = 'PT'
        btnPt.clicked.connect(self.setElement)

        btnNo = QPushButton(QIcon('img/not.png'), 'NOT')
        btnNo.toolTip = 'NOT'
        btnNo.clicked.connect(self.setElement)

        btnOr = QPushButton(QIcon('img/or.png'), 'OR')
        btnOr.toolTip = 'OR'
        btnOr.clicked.connect(self.setElement)

        btnAnd = QPushButton(QIcon('img/and.png'), 'AND')
        btnAnd.toolTip = 'AND'
        btnAnd.clicked.connect(self.setElement)

        btnIn = QPushButton(QIcon('img/in.png'), 'IN')
        btnIn.toolTip = 'IN'
        btnIn.clicked.connect(self.setElement)

        btnOut = QPushButton(QIcon('img/in.png'), 'OUT')
        btnOut.toolTip = 'OUT'
        btnOut.clicked.connect(self.setElement)

        btnCalc = QPushButton('Подсчитать')
        btnCalc.clicked.connect(self.calc)

        grid_box = QGridLayout()  # row, column, row_count, column_count
        grid_box.addWidget(btnWire, 0, 0, 1, 2)
        grid_box.addWidget(btnPt, 1, 0, 1, 1)
        grid_box.addWidget(btnNo, 1, 1, 1, 1)
        grid_box.addWidget(btnOr, 2, 0, 1, 1)
        grid_box.addWidget(btnAnd, 2, 1, 1, 1)
        grid_box.addWidget(btnIn, 3, 0, 1, 1)
        grid_box.addWidget(btnOut, 3, 1, 1, 1)
        # grid_box.addStretch(1)
        grid_box.addWidget(btnCalc, 5, 0, 1, 2)
        grid_box.addWidget(self.mresult, 6, 0, 10, 2)
        grid_box.addWidget(self.mcanvas, 0, 2, 10, 10)
        self.setLayout(grid_box)
        self.resize(800, 500)
        self.setStatus('Ready to work')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwin = QMainWindow()
    mainwin.setWindowTitle('AndORra - конструктор логических схем')
    main = MainWindow(mainwin.menuBar())
    main.loadScheme('123.el')
    mainwin.setCentralWidget(main)
    mainwin.show()
    st = app.exec_()
    print('exit')
    sys.exit(st)

