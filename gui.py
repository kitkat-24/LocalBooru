import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap

import LocalBooru as lb


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'LocalBooru'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create widget
        label = QLabel(self)
        pixmap = QPixmap('image.png')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())

        self.showMaximized()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
