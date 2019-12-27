import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

import LocalBooru as lb


class App(QWidget):
    def __init__(self, qapp):
        super().__init__()
        self.title = 'LocalBooru'
        self.qapp = qapp
        #self.left = 10
        #self.top = 10
        #self.width = 640
        #self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
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
    ex = App(app)
    sys.exit(app.exec_())
