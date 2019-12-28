import sys
from collections import namedtuple
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

import ImgButton as ib
import LocalBooru as lb

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

        # Create master widget + layout:
        # Core widget owns core layout, which owns sublayouts
        self.mainFrame = QFrame(self)
        self.mainLayout = QVBoxLayout(self.mainFrame)

        # Create menu widget + layout:
        # Widgets are owned by mainFrame, added to mainLayout
        self.topbarFrame = QFrame(self.mainFrame)
        self.mainLayout.addWidget(self.topbarFrame)
        self.topbarLayout = QHBoxLayout(self.topbarFrame)
        self.addTopbarButtons()
        #self.topbarFrame.show()

        # Create layout to hold main screen elements: lefthand tag column and
        # central image gallery/close-up view.
        self.centralFrame = QFrame(self.mainFrame)
        self.centralLayout = QHBoxLayout(self.centralFrame)

        # Create left column widget + layout:
        self.leftFrame = QFrame(self.centralFrame)
        self.centralLayout.addWidget(self.leftFrame)
        self.leftLayout = QVBoxLayout(self.leftFrame)
        # Populate column
        self.addLeftCol()
        #self.leftFrame.show()

        # Create image display grid widget + layout:
        self.imFrame = QFrame(self.centralFrame)
        self.centralLayout.addWidget(self.imFrame)
        self.imLayout = QGridLayout(self.imFrame)
        #self.imFrame.show()

        # Done
        #self.showMaximized()
        self.centralFrame.show()
        #self.show()

    def addTopbarButtons(self):
        """Populate the buttons in the topbar."""
        pixmap = QPixmap(icon_path + 'Plus.svg')
        pixmap = pixmap.scaled(
                menu_icon_size.width(),
                menu_icon_size.height(),
                transformMode=QtCore.Qt.SmoothTransformation)
        add_but = ib.ImgButton(pixmap, self.topbarFrame)
        add_but.clicked.connect(self.add_dialogue)
        #add_but.setSize(menu_icon_size)

        pixmap = QPixmap(icon_path + 'Share.svg')
        pixmap = pixmap.scaled(
                menu_icon_size.width(),
                menu_icon_size.height(),
                transformMode=QtCore.Qt.SmoothTransformation)
        share_but = ib.ImgButton(pixmap, self.topbarFrame)
        share_but.clicked.connect(self.share_dialogue)
        #share_but.setSize(menu_icon_size)

        pixmap = QPixmap(icon_path + 'Trash.svg')
        pixmap = pixmap.scaled(
                menu_icon_size.width(),
                menu_icon_size.height(),
                transformMode=QtCore.Qt.SmoothTransformation)
        delete_but = ib.ImgButton(pixmap, self.topbarFrame)
        delete_but.clicked.connect(self.delete_dialogue)
        #delete_but.setSize(menu_icon_size)

        self.search_query = QLineEdit()
        search_but = QPushButton('Search', self.topbarFrame)
        search_but.clicked.connect(self.search)

        # Add to topbar
        self.topbarLayout.addWidget(add_but, QLayout.SetMinimumSize)
        self.topbarLayout.addWidget(share_but, QLayout.SetMinimumSize)
        self.topbarLayout.addWidget(delete_but, QLayout.SetMinimumSize)
        self.topbarLayout.addWidget(self.search_query, QGridLayout.SetMaximumSize)
        self.topbarLayout.addWidget(search_but, QLayout.SetMinimumSize)

        # Stretch to fit
        self.topbarLayout.addStretch()

    def addLeftCol(self):
        """Populate the left column with tags."""
        for i in range(7):
            widget = QWidget(self.leftFrame)
            label = QLabel(widget)
            label.setText(f'bs tag {i}')
            widget.show()
            self.leftLayout.addWidget(widget, QLayout.SetMinimumSize)


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
