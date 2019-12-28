import sys
from collections import namedtuple
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

import LocalBooru as lb
import QtExtensions as QExt

thumbnail_size = QtCore.QSize(150, 150)
tag_width = 150
icon_path = './basic-ui-icons/SVGs/'
menu_icon_size = QtCore.QSize(64, 64)


class LBmain(QWidget):
    def __init__(self, qapp):
        super().__init__()
        self.title = 'LocalBooru'
        self.qapp = qapp
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        screen = self.qapp.desktop().screenGeometry()
        self.width, self.height = screen.width(), screen.height()
        self.resize(self.width, self.height)


        # Create menu widget + layout:
        # Widgets are owned by mainFrame, added to mainLayout
        self.topbarFrame = QFrame(self)
        self.topbarLayout = QHBoxLayout(self.topbarFrame)
        self.addTopbarButtons()

        # Create left column widget + layout:
        self.tagBox = QGroupBox('Tags')
        self.tagBox.setFixedWidth(tag_width)
        self.tagList = QExt.TagList()
        self.addLeftCol()
        self.tagList.itemClicked.connect(self.tagClicked)

        tagLayout = QVBoxLayout()
        tagLayout.addWidget(self.tagList, QtCore.Qt.MinimumSize)
        self.tagBox.setLayout(tagLayout)

        # Create image display grid widget + layout:
        self.imBox = QGroupBox('Images')
        imLayout = QGridLayout()
        self.displayThumbnails(imLayout)
        self.imBox.setLayout(imLayout)


        # Create layout to hold main screen elements: lefthand tag column and
        # central image gallery/close-up view.
        self.centralFrame = QFrame(self)
        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.tagBox)
        self.centralLayout.addWidget(self.imBox)


        # Create master layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.topbarFrame)
        self.mainLayout.addWidget(self.centralFrame)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Done
        #self.showMaximized()

        self.setLayout(self.mainLayout)
        self.show()

    #---------------------------------------------------------------------------
    # Section creation functions
    #---------------------------------------------------------------------------

    def addTopbarButtons(self):
        """Populate the buttons in the topbar."""
        pixmap = QPixmap(icon_path + 'Plus.svg')
        pixmap = pixmap.scaled(
                menu_icon_size.width(),
                menu_icon_size.height(),
                transformMode=QtCore.Qt.SmoothTransformation)
        add_but = QExt.ImgButton(pixmap, parent=self.topbarFrame)
        add_but.clicked.connect(self.add_dialogue)

        pixmap = QPixmap(icon_path + 'Share.svg')
        pixmap = pixmap.scaled(
                menu_icon_size.width(),
                menu_icon_size.height(),
                transformMode=QtCore.Qt.SmoothTransformation)
        share_but = QExt.ImgButton(pixmap, parent=self.topbarFrame)
        share_but.clicked.connect(self.share_dialogue)

        pixmap = QPixmap(icon_path + 'Trash.svg')
        pixmap = pixmap.scaled(
                menu_icon_size.width(),
                menu_icon_size.height(),
                transformMode=QtCore.Qt.SmoothTransformation)
        delete_but = QExt.ImgButton(pixmap, parent=self.topbarFrame)
        delete_but.clicked.connect(self.delete_dialogue)

        self.search_query = QLineEdit()
        search_but = QPushButton('Search', self.topbarFrame)
        search_but.clicked.connect(self.search)

        # Add to topbar
        self.topbarLayout.addWidget(add_but)
        self.topbarLayout.addWidget(share_but)
        self.topbarLayout.addWidget(delete_but)
        self.topbarLayout.addWidget(self.search_query)
        self.topbarLayout.addWidget(search_but)

        self.topbarLayout.setAlignment(QtCore.Qt.AlignVCenter)

        # Stretch to fit
        #self.topbarLayout.addStretch()

    def addLeftCol(self):
        """Populate the left column with tags."""
        for i in range(7):
            self.tagList.addItem(f'bs tag {i}')

    @QtCore.pyqtSlot(QListWidgetItem)
    def tagClicked(self, item):
        """Action when an item in the list is clicked.

        Usage: listWidget.itemClicked.connect(TagList.Clicked)
        """
        QMessageBox.information(self, "ListWidget", "You clicked: " + item.text())

    def scaleImg(self, pix: QPixmap, size: QtCore.QSize):
        """Scale an a QPixmap and maintain aspect ratio."""
        return pix.scaled(size.width(), size.height(),
                QtCore.Qt.KeepAspectRatio,
                transformMode=QtCore.Qt.SmoothTransformation)


    def displayThumbnails(self, layout):
        """Display grid of thumbnails."""
        cols = int((self.width - 150) / (1.25 * thumbnail_size.width()))
        rows = int((self.height - 150) / (1.25 * thumbnail_size.height()))

        # Dummy image
        pixmap = self.scaleImg(QPixmap('image.png'), thumbnail_size)

        for i in range(rows):
            # Setting min size will make empty rows display
            layout.setColumnMinimumWidth(i, thumbnail_size.width())
            layout.setRowMinimumHeight(i, thumbnail_size.height())
            for j in range(cols):
                label = QLabel()
                label.setPixmap(pixmap)
                layout.addWidget(label, i, j)




    #---------------------------------------------------------------------------
    # Button functions
    #---------------------------------------------------------------------------
    def add_dialogue(self):
        """Begin dialogue to add an image to the database."""
        alert = QMessageBox()
        alert.setText('You clicked the add button!')
        alert.exec_()

    def share_dialogue(self):
        """Begin dialogue to export an image from the database."""
        alert = QMessageBox()
        alert.setText('You clicked the share button!')
        alert.exec_()

    def delete_dialogue(self):
        """Begin dialogue to remove an image from the database."""
        alert = QMessageBox()
        alert.setText('You clicked the delete button!')
        alert.exec_()

    def search(self):
        """Perform a database search."""
        alert = QMessageBox()
        alert.setText('You searched for: {}!'.format(self.search_query.text()))
        alert.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    lbm = LBmain(app)
    sys.exit(app.exec_())
