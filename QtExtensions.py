from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter
from PyQt5 import QtCore

class ImgButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(ImgButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        if hasattr(self, 'prefImSize'):
            return self.prefImSize
        else:
            return self.pixmap.size()

    def setSize(self, size):
        self.prefImSize = size


class TagList(QListWidget):
    def __init__(self, parent=None):
        super(QListWidget, self).__init__(parent)
