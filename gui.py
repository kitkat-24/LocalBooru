import sys
from collections import namedtuple
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

import LocalBooru as lb
import QtExtensions as QExt

thumbnail_size = QtCore.QSize(100, 100)
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
        width, height = screen.width(), screen.height()
        self.resize(width, height)


        # Create menu widget + layout:
        # Widgets are owned by mainFrame, added to mainLayout
        self.topbarFrame = QFrame(self)
        self.topbarLayout = QHBoxLayout(self.topbarFrame)
        self.addTopbarButtons()

        # Create layout to hold main screen elements: lefthand tag column and
        # central image gallery/close-up view.
        self.centralFrame = QFrame(self)
        self.centralLayout = QHBoxLayout(self.centralFrame)

        # Create left column widget + layout:
        self.tagBox = QGroupBox('Tags')
        layout = QVBoxLayout()
        self.tagList = QExt.TagList()
        self.centralLayout.addWidget(self.tagBox)
        # Populate column
        self.addLeftCol()
        self.tagList.itemClicked.connect(self.tagClicked)
        self.tagList.show()
        layout.addWidget(self.tagList)
        self.tagBox.setLayout(layout)

        # Create image display grid widget + layout:
        self.imFrame = QFrame(self.centralFrame)
        self.centralLayout.addWidget(self.imFrame)
        self.imLayout = QGridLayout(self.imFrame)



        # Create master layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.topbarFrame)
        self.mainLayout.addWidget(self.centralFrame)

        # Done
        #self.showMaximized()
        self.setLayout(self.mainLayout)
        self.show()

    def addTopbarButtons(self):
        """Populate the buttons in the topbar."""
        pixmap = QPixmap(icon_path + 'Plus.svg')
        pixmap = pixmap.scaled(
                menu_icon_size.width(),
                menu_icon_size.height(),
                transformMode=QtCore.Qt.SmoothTransformation)
        add_but = QExt.ImgButton(pixmap, self.topbarFrame)
        add_but.clicked.connect(self.add_dialogue)

        pixmap = QPixmap(icon_path + 'Share.svg')
        pixmap = pixmap.scaled(
                menu_icon_size.width(),
                menu_icon_size.height(),
                transformMode=QtCore.Qt.SmoothTransformation)
        share_but = QExt.ImgButton(pixmap, self.topbarFrame)
        share_but.clicked.connect(self.share_dialogue)

        pixmap = QPixmap(icon_path + 'Trash.svg')
        pixmap = pixmap.scaled(
                menu_icon_size.width(),
                menu_icon_size.height(),
                transformMode=QtCore.Qt.SmoothTransformation)
        delete_but = QExt.ImgButton(pixmap, self.topbarFrame)
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
