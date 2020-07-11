#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow,QAction, QApplication, qApp
from PyQt5.QtGui import QIcon

class Example(QMainWindow):
  def __init__(self):
    super().__init__()

    self.initUI()

  def initUI(self):
    exitAct = QAction(QIcon('exit.png'),' &Exit',self)
    exitAct.setShortcut('Ctrl+Q')
    exitAct.setStatusTip("Exit application")
    exitAct.triggered.connect(qApp.quit)

    aboutAct = QAction(QIcon('exit.png'), 'About',self)
    aboutAct.setStatusTip("About the app")

    self.statusBar()

    menubar = self.menuBar()
    menubar.setNativeMenuBar(False)

    fileMenu = menubar.addMenu("&File")
    fileMenu.addAction(aboutAct)
    #fileMenu.addAction(exitAct)

    self.setGeometry(300,300,300,200)
    self.setWindowTitle("Simple menu")
    self.show()

if __name__ == '__main__':

  app = QApplication(sys.argv)

  ex = Example()

  sys.exit(app.exec_())
