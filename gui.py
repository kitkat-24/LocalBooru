import sys
from collections import namedtuple
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

import LocalBooru as lb

Dimension = namedtuple('Dimension', 'w h')
thumbnail = Dimension(100, 100)


class LBmain(QMainWindow):
    def __init__(self, qapp):
        super().__init__()
        self.title = 'LocalBooru'
        self.qapp = qapp
        self.initUI()

    def initUI(self):
        # Create menubar
        aboutAct = QAction(QIcon('exit.png'), 'About',self)
        aboutAct.setStatusTip("About the app")
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(aboutAct)

        self.setWindowTitle(self.title)
        layout = QVBoxLayout()

        #self.setGeometry(self.left, self.top, self.width, self.height)

        screen = self.qapp.desktop().screenGeometry()
        width, height = screen.width(), screen.height()

        # Create widget
        label = QLabel(self)
        pixmap = QPixmap('image.png')
        pixmap = pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        self.showMaximized()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    lbm = LBmain(app)
    sys.exit(app.exec_())
