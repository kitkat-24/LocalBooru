import sys
from collections import namedtuple
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QMessageBox, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

import LocalBooru as lb

Dimension = namedtuple('Dimension', 'w h')
thumbnail = Dimension(100, 100)
icon_path = './basic-ui-icons/SVGs/'
menu_icon_size = QtCore.QSize(48, 48)
menu_button_size = QtCore.QSize(menu_icon_size.width() + 8, menu_icon_size.height() + 8)
print(menu_button_size)


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
        self.topbarFrame.show()




        #mainseg = QHBoxLayout()
        #leftcol = QVBoxLayout()
        #browser = QGridLayout(self)

        # Done
        #self.showMaximized()
        self.show()

    def addTopbarButtons(self):
        """Populate the buttons in the topbar."""
        add_but = QPushButton('', self.topbarFrame)
        add_but.clicked.connect(self.add_dialogue)
        add_but.setIcon(QIcon(icon_path + 'Plus.svg'))
        add_but.setIconSize(menu_icon_size)

        share_but = QPushButton('', self.topbarFrame)
        share_but.clicked.connect(self.share_dialogue)
        share_but.setIcon(QIcon(icon_path + 'Share.svg'))
        share_but.setIconSize(menu_icon_size)

        delete_but = QPushButton('', self.topbarFrame)
        delete_but.clicked.connect(self.delete_dialogue)
        delete_but.setIcon(QIcon(icon_path + 'Trash.svg'))
        delete_but.setIconSize(menu_icon_size)

        self.search_query = QLineEdit()
        search_but = QPushButton('Search', self.topbarFrame)
        search_but.clicked.connect(self.search)

        # Add to topbar
        self.topbarLayout.addWidget(add_but, QtWidgets.QLayout.SetMinimumSize)
        self.topbarLayout.addWidget(share_but, QtWidgets.QLayout.SetMinimumSize)
        self.topbarLayout.addWidget(delete_but, QtWidgets.QLayout.SetMinimumSize)
        self.topbarLayout.addWidget(self.search_query, QtWidgets.QGridLayout.SetMaximumSize)
        self.topbarLayout.addWidget(search_but, QtWidgets.QLayout.SetMinimumSize)

        # Stretch to fit
        self.topbarLayout.addStretch()


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
    lbm = LBmain(app)
    sys.exit(app.exec_())
