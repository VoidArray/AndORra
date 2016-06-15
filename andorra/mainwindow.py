import sys
import pickle

from PyQt5.QtWidgets import QAction, QMainWindow
from PyQt5.QtGui import QIcon

from andorra.central_widget import CentralWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setMinimumHeight(500)
        self.setMinimumWidth(800)
        self.setWindowTitle('AndORra - конструктор схем')
        self.menubar = self.menuBar()
        self.central_widget = CentralWidget(self.setStatus)

        # init menu
        actionWire = QAction(QIcon('img/wire.png'), 'Wire', self)
        actionWire.setShortcut('w')
        actionWire.setStatusTip('Connect elements')
        actionWire.toolTip = 'WIRE'
        actionWire.triggered.connect(self.central_widget.setElement)

        actionPt = QAction(QIcon('img/point.png'), 'Point', self)
        actionPt.setShortcut('p')
        actionPt.toolTip = 'PT'
        actionPt.triggered.connect(self.central_widget.setElement)

        actionNo = QAction(QIcon('img/no.png'), 'NOT', self)
        actionNo.toolTip = 'NOT'
        actionNo.setShortcut('n')
        actionNo.triggered.connect(self.central_widget.setElement)

        actionOr = QAction(QIcon('img/or.png'), 'OR', self)
        actionOr.toolTip = 'OR'
        actionOr.setShortcut('r')
        actionOr.triggered.connect(self.central_widget.setElement)

        actionAnd = QAction(QIcon('img/and.png'), 'AND', self)
        actionAnd.toolTip = 'AND'
        actionAnd.setShortcut('a')
        actionAnd.triggered.connect(self.central_widget.setElement)

        actionIn = QAction(QIcon('img/in.png'), 'IN', self)
        actionIn.toolTip = 'IN'
        actionIn.setShortcut('i')
        actionIn.triggered.connect(self.central_widget.setElement)

        actionOut = QAction(QIcon('img/out.png'), 'OUT', self)
        actionOut.toolTip = 'OUT'
        actionOut.setShortcut('e')
        actionOut.triggered.connect(self.central_widget.setElement)

        actionCalc = QAction(QIcon('img/point.png'), 'Подсчитать', self)
        actionCalc.setShortcut('ctrl+c')
        actionCalc.triggered.connect(self.central_widget.calc)

        actionSaveScheme = QAction(QIcon('img/point.png'), 'Сохранить в файл', self)
        actionSaveScheme.setShortcut('ctrl+s')
        actionSaveScheme.triggered.connect(self.central_widget.saveFileDialog)

        actionLoadScheme = QAction(QIcon('img/point.png'), 'Загрузить файл', self)
        actionLoadScheme.setShortcut('ctrl+o')
        actionLoadScheme.triggered.connect(self.central_widget.openFileDialog)

        # actionSave = QPushButton('Save')
        # actionSave.setShortcut('ctrl+s')
        # actionSave.triggered.connect(self.saveLogic)

        actionQuit = QAction(QIcon('img/point.png'), 'Выход', self)
        actionQuit.setShortcut('ctrl+q')
        actionQuit.triggered.connect(quit)

        actionClear = QAction(QIcon('img/point.png'), 'Очистить', self)
        actionClear.setShortcut('ctrl+del')
        actionClear.triggered.connect(self.central_widget.clearScheme)

        schemeMenu = self.menubar.addMenu('&Схема')
        schemeMenu.addAction(actionCalc)
        schemeMenu.addAction(actionSaveScheme)
        schemeMenu.addAction(actionLoadScheme)
        schemeMenu.addAction(actionClear)
        schemeMenu.addAction(actionQuit)

        elemMenu = self.menubar.addMenu('&Элементы')
        elemMenu.addAction(actionWire)
        elemMenu.addAction(actionIn)
        elemMenu.addAction(actionOut)
        elemMenu.addAction(actionOr)
        elemMenu.addAction(actionAnd)
        elemMenu.addAction(actionPt)

        optionsMenu = self.menubar.addMenu('&Настройки')

        self.resize(800, 500)
        self.setCentralWidget(self.central_widget)
        self.setStatus('Готов к работе')

    def setStatus(self, status):
        self.statusBar().showMessage(status)

    def loadScheme(self, fileName):
        """
        загрузка графической схемы
        """
        self.central_widget.loadScheme(fileName)
        self.setStatus('Схема загружена' + fileName)
