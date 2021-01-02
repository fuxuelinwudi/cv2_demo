# -*- coding: utf-8 -*-

import cv2
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, \
    QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem, QInputDialog, QLineEdit
import numpy as np
import sys
import matplotlib.pyplot as plt
from ui.graphdesign_ui import *

class bianji_MainWindow(QMainWindow,Ui_graphdesign):

    def __init__(self, parent=None):
        super(bianji_MainWindow, self).__init__(parent)
        self.setupUi(self)

    # 放大图片
    def on_zoomout_clicked(self):
        self.label.setText("放大")
        # TODO: not implemented yet
        self.zoomscale = self.zoomscale + 0.05
        if self.zoomscale >= 1.2:
            self.zoomscale = 1.2
        self.item.setScale(self.zoomscale)

    # 缩小图片
    def on_zoomin_clicked(self):
        self.label.setText("缩小")
        # TODO: not implemented yet
        self.zoomscale = self.zoomscale - 0.05
        if self.zoomscale <= 0:
            self.zoomscale = 0.2
        self.item.setScale(self.zoomscale)

    # 拖拽图片
    def dragLeaveEvent(self, event):
        self.dragOver = False
        self.update()

    def dropEvent(self, event):
        self.dragOver = False
        self.update()

    # 保存图片
    def call_back_action_store_func(self):
        # 用 QFileDialog 获取保存文件的全部路径（包括文件名和后缀名）
        fileName2, ok2 = QFileDialog.getSaveFileName(self, "文件保存", "/", "图片文件 (*.png);;(*.jpeg)")
        """
        下面用 Pyqt5 的截屏方法，截取指定 QChartView 上显示的东西；缺点，若显示的图像变形，
        则截图也会变形！
        """
        screen = QApplication.primaryScreen()
        pix = screen.grabWindow(self.graphicsView.winId())
        pix.save(fileName2)
        print("已成功保存图片至"+fileName2)

    # 旋转图片
    def right_rotate(self):
        self.label.setText("右旋")
        self.graphicsView.rotate(90)
    def left_rotate(self):
        self.label.setText("左旋")
        self.graphicsView.rotate(-90)

    # 打开图片
    def select_button_clicked(self):
        self.label.setText("请进行编辑!")
        self.graphicsView.clearFocus()
        global image_path
        count = 0
        while count < 1:
            file_name = QFileDialog.getOpenFileName(self, "Open File", "./", "jpg (*.jpg)")
            image_path = file_name[count]
            if (file_name[count] == ""):
                QMessageBox.information(self, "提示", self.tr("请选择图片文件！"))
                break
            img = cv2.imread(image_path)  # 读取图像
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像通道
            x = img.shape[1]  # 获取图像大小
            y = img.shape[0]
            self.zoomscale = 1  # 图片放缩尺度
            frame = QImage(img, x, y, x * 3, QImage.Format_RGB888)
            pix = QPixmap.fromImage(frame)
            self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
            self.item.setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动，非常关键！！！！！
            self.scene = QGraphicsScene()  # 创建场景
            self.scene.addItem(self.item)
            self.graphicsView.setScene(self.scene)
            count = count + 1

    # 灰度图
    def to_gray(self):
        self.label.setText("灰度图")
        #self.graphicsView.clearFocus()
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, x * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动，非常关键！！！！！
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)

    # 平滑处理
    def filter(self):
        self.label.setText("平滑处理")
        MEAN_FILTER = 0
        GAUSSIAN_FILTER = 1
        MEDIAN_FILTER = 2
        self._ksize = 3
        self._kind = MEAN_FILTER
        self._sigmax = 0
        img = cv2.imread(image_path)
        if self._kind == MEAN_FILTER:
            img = cv2.blur(img, (self._ksize, self._ksize))
        elif self._kind == GAUSSIAN_FILTER:
            img = cv2.GaussianBlur(img, (self._ksize, self._ksize), self._sigmax)
        elif self._kind == MEDIAN_FILTER:
            img = cv2.medianBlur(img, self._ksize)

        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, x * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动，非常关键！！！！！
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)

    # 亮度调节
    def image_hist_demo(self):
        self.label.setText("亮度调节")
        item1, ok = QInputDialog.getDouble(self, "输入alpha值", "alpha值：", 1, 0, 3)
        if ok:
            self._alpha = item1
        else:
            self._alpha = 1
        item2, ok1 = QInputDialog.getDouble(self, "输入beta值", "beta值：", 0, 0, 1000000000)
        if ok1:
            self._beta = item2
        else:
            self._beta = 0
        img = cv2.imread(image_path)
        blank = np.zeros(img.shape, img.dtype)
        img = cv2.addWeighted(img, self._alpha, blank, 1 - self._alpha, self._beta)
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, x * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动，非常关键！！！！！
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)

    # 形态学
    def morph(self):
        self.label.setText("形态学")
        ERODE_MORPH_OP = 0
        DILATE_MORPH_OP = 1
        OPEN_MORPH_OP = 2
        CLOSE_MORPH_OP = 3
        GRADIENT_MORPH_OP = 4
        TOPHAT_MORPH_OP = 5
        BLACKHAT_MORPH_OP = 6

        RECT_MORPH_SHAPE = 0
        CROSS_MORPH_SHAPE = 1
        ELLIPSE_MORPH_SHAPE = 2

        MORPH_OP = {
            ERODE_MORPH_OP: cv2.MORPH_ERODE,
            DILATE_MORPH_OP: cv2.MORPH_DILATE,
            OPEN_MORPH_OP: cv2.MORPH_OPEN,
            CLOSE_MORPH_OP: cv2.MORPH_CLOSE,
            GRADIENT_MORPH_OP: cv2.MORPH_GRADIENT,
            TOPHAT_MORPH_OP: cv2.MORPH_TOPHAT,
            BLACKHAT_MORPH_OP: cv2.MORPH_BLACKHAT
        }

        MORPH_SHAPE = {
            RECT_MORPH_SHAPE: cv2.MORPH_RECT,
            CROSS_MORPH_SHAPE: cv2.MORPH_CROSS,
            ELLIPSE_MORPH_SHAPE: cv2.MORPH_ELLIPSE
        }

        self._ksize = 3
        self._op = ERODE_MORPH_OP
        self._kshape = RECT_MORPH_SHAPE

        op = MORPH_OP[self._op]
        kshape = MORPH_SHAPE[self._kshape]
        kernal = cv2.getStructuringElement(kshape, (self._ksize, self._ksize))
        img = cv2.imread(image_path)
        img = cv2.morphologyEx(img, self._op, kernal)
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, x * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动，非常关键！！！！！
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)

    # 卷积降噪
    def jiangzao(self):
        self.label.setText("卷积降噪")
        im = cv2.imread(image_path)
        kernel = np.array([[0, -1, 0], [0, 5, 0], [0, -1, 0]])  # 自定义了卷积核，对每一个像素进行操作
        img = cv2.filter2D(im, -1, kernel)
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, x * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动，非常关键！！！！！
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)

    # 恢复原图
    def resetgraph(self):
        self.label.setText("已恢复原图！")
        self.graphicsView.clearFocus()
        img = cv2.imread(image_path)  # 读取图像
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像通道
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, x * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动，非常关键！！！！！
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)

    # 伽马校正
    def gammacorrect(self):
        self.label.setText("伽马校正")
        age, ok = QInputDialog.getInt(self, "gamma值","请输入gamma值:",QLineEdit.Normal)
        if ok:
            self._gamma = age
        else:
            self._gamma = 1
        gamma_table = [np.power(x / 255.0,self._gamma) * 255.0 for x in range(256)]
        gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
        img = cv2.imread(image_path)
        img = cv2.LUT(img,gamma_table)
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, x * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动，非常关键！！！！！
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)

    # 边缘检测
    def edgetest(self):
        self.label.setText("边缘检测")
        item1, ok = QInputDialog.getDouble(self, "输入阈值1", "阈值1：", 20, 0, 255)
        if ok:
            self._thresh1 = item1
        else:
            self._thresh1 = 20
        item2, ok1 = QInputDialog.getDouble(self, "输入阈值2", "阈值2：", 100, 0, 255)
        if ok1:
            self._thresh2 = item2
        else:
            self._thresh2 = 100
        img = cv2.imread(image_path)
        img = cv2.Canny(img, threshold1=self._thresh1, threshold2=self._thresh2)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, x * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动，非常关键！！！！！
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)

    # 图像梯度
    def gradtest(self):
        self.label.setText("图像梯度")
        item1, ok = QInputDialog.getInt(self, "输入核大小", "核大小：", 3, 1, 1000000)
        if ok:
            self._ksize = item1
        else:
            self._ksize = 3
        item2, ok1 = QInputDialog.getInt(self, "输入x方向", "x大小：", 1, 0, 1)
        if ok1:
            self._dx = item2
        else:
            self._dx = 1
        item3, ok = QInputDialog.getInt(self, "输入y方向", "y大小：", 0, 0, 1)
        if ok:
            self._dy = item3
        else:
            self._dy = 0
        SOBEL_GRAD = 0
        SCHARR_GRAD = 1
        LAPLACIAN_GRAD = 2
        self._kind = SOBEL_GRAD
        img = cv2.imread(image_path)
        if self._dx == 0 and self._dy == 0 and self._kind != LAPLACIAN_GRAD:
            self.setBackground(QColor(255, 0, 0))
            self.setText('图像梯度 （无效: dx与dy不同时为0）')
        else:
            if self._kind == SOBEL_GRAD:
                img = cv2.Sobel(img, -1, self._dx, self._dy, self._ksize)
            elif self._kind == SCHARR_GRAD:
                img = cv2.Scharr(img, -1, self._dx, self._dy)
            elif self._kind == LAPLACIAN_GRAD:
                img = cv2.Laplacian(img, -1)
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, x * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动，非常关键！！！！！
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)

    # 查看直方图
    def histogram(self):
        img = cv2.imread(image_path)
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histr = cv2.calcHist([img], [i], None, [256], [0, 256])
            histr = histr.flatten()
            plt.plot(range(256), histr, color=col)
            plt.xlim([0, 256])
        plt.show()

    # 退出
    def call_back_action_close_func(self):
        self.close()
        print("编辑窗口已关闭")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    bj = bianji_MainWindow()
    bj.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
