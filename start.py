import sys

from PyQt5.QtWidgets import QApplication

from andorra.mainwindow import MainWindow


app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.setWindowTitle('AndORra - конструктор логических схем')
mainwindow.loadScheme('schemes/and_or.el')
mainwindow.show()
st = app.exec_()
print('exit')
sys.exit(st)