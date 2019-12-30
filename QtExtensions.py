from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter
from PyQt5 import QtCore

class ImgButton(QAbstractButton):
    def __init__(self, pixmap, pixmap_hover=None, pixmap_pressed=None, parent=None):
        super(ImgButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover if pixmap_hover else pixmap
        self.pixmap_pressed = pixmap_pressed if pixmap_pressed else pixmap

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.preferredSize = None

    def setPixmap(self, pixmap, pixmap_hover=None, pixmap_pressed=None):
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover if pixmap_hover else pixmap
        self.pixmap_pressed = pixmap_pressed if pixmap_pressed else pixmap

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return self.preferredSize if self.preferredSize else self.pixmap.size()

    def size(self):
        return self.preferredSize if self.preferredSize else self.pixmap.size()

    def setSize(self, size):
        self.prefImSize = size


class TagList(QListWidget):
    def __init__(self, parent=None):
        super(QListWidget, self).__init__(parent)
