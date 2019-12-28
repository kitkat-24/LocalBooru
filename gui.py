import sys
from collections import namedtuple
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

import LocalBooru as lb

Dimension = namedtuple('Dimension', 'w h')
thumbnail = Dimension(100, 100)
icon_path = './basic-ui-icons/SVGs/'
menu_icon_size = QtCore.QSize(24,24)


class LBmain(QMainWindow):
    def __init__(self, qapp):
        super().__init__()
        self.title = 'LocalBooru'
        self.qapp = qapp
        self.initUI()

    def initUI(self):
        ## Create menubar
        #aboutAct = QAction(QIcon('exit.png'), 'About',self)
        #aboutAct.setStatusTip("About the app")
        #menubar = self.menuBar()
        #menubar.setNativeMenuBar(False)
        #fileMenu = menubar.addMenu("&File")
        #fileMenu.addAction(aboutAct)

        self.setWindowTitle(self.title)

        # Create master widget + layout:
        # Core widget owns core layout, which owns sublayouts
        self.mainFrame = QtWidgets.QFrame(self)
        self.mainLayout = QVBoxLayout(self.mainFrame)
        self.setCentralWidget(self.mainFrame)

        # Create menu widget + layout:
        # Widgets are owned by mainFrame, added to mainLayout
        self.topbarFrame = QtWidgets.QFrame(self.mainFrame)
        self.mainLayout.addWidget(self.topBarFrame)
        self.topbarLayout = QHBoxLayout(self.topbarFrame)
        # Segment code
        self.addTopbarButtons()
        self.topbarFrame.show()




        mainseg = QHBoxLayout()
        leftcol = QVBoxLayout()
        browser = QGridLayout(self)




        #self.setGeometry(self.left, self.top, self.width, self.height)

        screen = self.qapp.desktop().screenGeometry()
        width, height = screen.width(), screen.height()

        # Create widget
        label = QLabel(self)
        pixmap = QPixmap('image.png')
        pixmap = pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        self.showMaximized()

    def addTopbarButtons(self):
        """Populate the buttons in the topbar."""
        add_but = QPushButton('', self)
        add_but.clicked.connect(self.add_dialogue)
        add_but.setIcon(QtGui.QIcon(icon_path + 'Plus.svg'))
        add_but.setIconSize(menu_icon_size)

        share_but = QPushButton('', self)
        share_but.clicked.connect(self.share_dialogue)
        share_but.setIcon(QtGui.QIcon(icon_path + 'Share.svg'))
        share_but.setIconSize(menu_icon_size)

        delete_but = QPushButton('', self)
        delete_but.clicked.connect(self.delete_dialogue)
        delete_but.setIcon(QtGui.QIcon(icon_path + 'Trash.svg'))
        delete_but.setIconSize(menu_icon_size)

        # Add to topbar
        self.topbarLayout.addWidget(add_but)
        self.topbarLayout.addWidget(share_but)
        self.topbarLayout.addWidget(delete_but)


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    lbm = LBmain(app)
    sys.exit(app.exec_())
