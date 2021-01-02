# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from numpy import *

from ui.graph_ui import *
from custom.graphdesign import *


class graph_MainWindow(QtWidgets.QMainWindow, Ui_graph):
    def __init__(self, parent=None):
        super().__init__(parent)  # 父类的构造函数
        self.timer_camera = QtCore.QTimer()  # 定时器
        self.cap = cv2.VideoCapture()  # 准备获取图像
        self.CAM_NUM = 0
        self.setupUi(self)  # 初始化程序界面
        self.initUI()  # 界面绘制交给InitUi方法

    #  设置摄像头分辨率
    def fbl(self):
        self.label1.setText("")
        global _weight
        global _height
        item1, ok = QInputDialog.getInt(self, "输入宽的值", "宽为：", 800, 320, 1080)
        if ok:
            _weight = item1
            print("当前分辨率宽为：",_weight)
        item2, ok = QInputDialog.getInt(self, "输入高的值", "高为：", 600, 240, 800)
        if ok:
            _height = item2
            print("当前分辨率高为：",_height)
    # 打开摄像头
    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(
                    self, u"Warning", u"请检测相机与电脑是否连接正确",
                    buttons=QtWidgets.QMessageBox.Ok,
                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
                self.pushButton.setText('关闭相机')
        else:
            self.timer_camera.stop()  # 关闭定时器
            self.cap.release()  # 释放视频流
            self.label.clear()  # 清空视频显示区域
            self.pushButton.setText('打开相机')

    # 显示图像
    def show_camera(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)  # 获取视频帧数
        flag, self.image = self.cap.read()
        self.image = cv2.flip(self.image, 1)  # 左右翻转
        show = cv2.resize(self.image, (_weight, _height))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))

    # 拍照
    def takePhoto(self):
        if self.timer_camera.isActive() != False:
            flag = 0
            cv2.putText(self.image,
                        (int(self.image.shape[1] / 2 - 130), int(self.image.shape[0] / 2)),
                        cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
                        1.0, (255, 0, 0), 1)
            self.timer_camera.stop()
            show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # 左右翻转
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))
            self.label.setScaledContents(True)
            self.pushButton_2.setText('保存此照片')
        else:
            flag = 1
            fileName2, ok2 = QFileDialog.getSaveFileName(self, "文件保存", "/", "图片文件 (*.png);;(*.jpeg)")
            screen = QApplication.primaryScreen()
            pix = screen.grabWindow(self.label.winId())
            pix.save(fileName2)
            self.pushButton_2.setText('拍照')
            self.pushButton.setText('切回相机')

    # 保存图片
    def call_back_action_store_func(self):
        fileName2, ok2 = QFileDialog.getSaveFileName(self, "文件保存", "/", "图片文件 (*.png);;(*.jpeg)")
        """
        下面用 Pyqt5 的截屏方法，截取指定 QChartView 上显示的东西；缺点，若显示的图像变形，
        则截图也会变形！
        """
        screen = QApplication.primaryScreen()
        pix = screen.grabWindow(self.graphicsView.winId())
        pix.save(fileName2)

    # 关闭窗口
    def call_back_action_close_func(self):
        self.close()
        MainWindow.close()
        print("图像处理窗口已关闭")

    # 跳转
    def to_bianji(self):
        bj.show()
        self.close()


app = QApplication(sys.argv)
MainWindow = QMainWindow()
gra = graph_MainWindow()
bj = bianji_MainWindow()
gra.setupUi(MainWindow)
