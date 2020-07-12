# Custom PyQt5 classes for the LocalBooru GUI
# Katerina R, July 2020

import re

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
        self.list_of_tags = []

    # TODO tags will not show up until you exit zoom view then re-enter it
    def updateTags(self, tags):
        """Update the tags displayed in the lefthand column."""
        self.clear()
        self.list_of_tags = tags
        if tags:
            for t in tags:
                self.addItem(t)
            for i in range(self.count()):
                self.item(i).setHidden(False)


class EditTagDialog(QDialog):
    def __init__(self, tags, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        tag_list = '; '.join(tags)
        self.tagBox = QTextEdit(tag_list, parent=self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);
        layout.addWidget(self.tagBox)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getUpdatedTags(self):
        """Returns the updated tags as a set."""
        return set(re.split('[;\s]+', self.tagBox.toPlainText().strip()))


class AddFileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.artist = QLineEdit(self)
        self.characters = QLineEdit(self)
        self.rating = QLineEdit(self)
        self.series = QLineEdit(self)
        self.tags = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addRow('Artist', self.artist)
        layout.addRow('Characters', self.characters)
        layout.addRow('Rating', self.rating)
        layout.addRow('Series', self.series)
        layout.addRow('Tags', self.tags)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getFileParams(self):
        """Returns a list of tags based on the input dialog (formatted for
        convenience to use with LocalBooru.py)."""
        params = []
        if self.artist.text():
            params += ['-a', self.artist.text()]
        if self.characters.text():
            chars = self.characters.text().split()
            for c in chars:
                params += ['-c', c]
        if self.rating.text():
            params += ['-r', self.rating.text()]
        if self.series.text():
            ss = self.series.text().split()
            for s in ss:
                params += ['-s', s]
        if self.tags.text():
            params += self.tags.text().split()

        return params
