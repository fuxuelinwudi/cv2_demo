# -*- coding: utf-8 -*-
import sys
import os
import time
import threading
from datetime import datetime
import wave
import pyaudio
from PyQt5.QtCore import QUrl

from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QFileDialog
from ui.voice_ui import *


class Player(object):

    def __init__(self, file, chunk=1024):
        self.file = file
        self.CHUNK = chunk

    def get_duration(self):
        """获取文件时长"""

        with wave.open(self.file) as df:
            rate = df.getframerate()
            frames = df.getnframes()
            return round(frames / float(rate))

    def __play(self):
        with wave.open(self.file) as wf:
            player = pyaudio.PyAudio()
            stream = player.open(format=player.get_format_from_width(wf.getsampwidth()),
                                 channels=wf.getnchannels(),
                                 rate=wf.getframerate(),
                                 output=True)
            data = wf.readframes(self.CHUNK)
            while data:
                stream.write(data)
                data = wf.readframes(self.CHUNK)
            stream.stop_stream()
            stream.close()
            player.terminate()

    def __timer(self):
        print("正在播放……")
        for t in range(int(self.get_duration())):
            print("\r剩余时间：%d" % (int(self.get_duration()) - t), end='')
            time.sleep(1)
        print("\r播放结束！")

    def __call__(self, *args, **kwargs):

        player = threading.Thread(target=self.__play)
        timer = threading.Thread(target=self.__timer)
        player.start()
        timer.start()
        player.join()
        timer.join()


class voice_MainWindow(QMainWindow, Ui_voice):
    def __init__(self):
        super(voice_MainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def luyin(self):

        # 创建目录
        if not os.path.exists('record'):
            os.makedirs('record')

        CHUNK = 512
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        rec_time = 10
        item1, ok = QInputDialog.getInt(self, "输入秒数", "秒数为：", 30, 5, 3600)
        if ok:
            rec_time = item1

        WAVE_OUTPUT_FILENAME = "record/" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".wav"
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        frames = []

        for i in range(0, int(RATE / CHUNK * rec_time)):  # 控制录音时间
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def playvoice(self):
        file_name = "test.wav"
        item1, ok = QInputDialog.getText(self, "输入要开的音频路径", "路径为：")
        if ok:
            file_name = item1
        p = Player(file_name)
        p()

    def tuichu(self):
        self.close()
        print("音频处理窗口已关闭")


app = QApplication(sys.argv)
MainWindow = QMainWindow()
voi = voice_MainWindow()
voi.setupUi(MainWindow)
