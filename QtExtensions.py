from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter
from PyQt5 import QtCore
from PyQt5.Qt import Qt

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


class ImageLabel(QLabel):
    def __init__(self, parent=None, onClick=None):
        super(ImageLabel, self).__init__(parent)
        self.onClick = onClick

        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setScaledContents(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.onClick:
                self.onClick()


class TagList(QListWidget):
    def __init__(self, parent=None):
        super(QListWidget, self).__init__(parent)

    def updateTags(self, tags):
        """Update the tags displayed in the lefthand column."""
        self.clear()
        if tags:
            for t in tags:
                self.addItem(t)
