from PyQt5.QtCore import QTimer

from ui.start_ui import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressDialog

from custom.voice1 import *
from custom.graph import *



class start_MainWindow(QtWidgets.QMainWindow, Ui_start):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    #跳转页面
    def word_get(self):
        gra.show()
        #MainWindow.close()

    def word_get1(self):
        voi.show()
        #MainWindow.close()


    def aqtuichu(self):
        MainWindow.close()
        print("您已安全退出")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()

    st = start_MainWindow()
    gra = graph_MainWindow()
    voi = voice_MainWindow()


    st.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())