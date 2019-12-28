from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter

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
    def Clicked(self,item):
        """Action when an item in the list is clicked.

        Usage: listWidget.itemClicked.connect(listWidget.Clicked)
        """
        QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())
