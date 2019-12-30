import sys
from collections import namedtuple
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
import random

import LocalBooru as lb
import QtExtensions as QExt

thumbnail_size = QtCore.QSize(150, 150)
tag_width = 150
icon_path = './basic-ui-icons/SVGs/'
menu_icon_size = QtCore.QSize(64, 64)


class LBmain(QMainWindow):
    def __init__(self, qapp):
        super().__init__()
        self.title = 'LocalBooru'
        self.qapp = qapp
        self.scaleFactor = 0.0
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
        self.imLayout = QGridLayout()
        self.displayThumbnails(self.imLayout)
        self.imBox.setLayout(self.imLayout)

        # Create image zoom display
        self.imZoomBox = QGroupBox('Image')
        self.imZoomLayout = QVBoxLayout()

        dummypix = QPixmap('image.png')
        self.imageLabel = QExt.ImgButton(pixmap=dummypix)
        self.imageLabel.clicked.connect(self.unenlarge)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.imageLabel)
        self.imZoomLayout.addWidget(self.scrollArea)
        self.imZoomBox.setLayout(self.imZoomLayout)
        self.imZoomBox.hide()


        # Create layout to hold main screen elements: lefthand tag column and
        # central image gallery/close-up view.
        self.centralFrame = QFrame(self)
        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.tagBox)
        self.centralLayout.addWidget(self.imBox)
        self.centralLayout.addWidget(self.imZoomBox)


        # Create master layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.topbarFrame)
        self.mainLayout.addWidget(self.centralFrame)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)


        # Final setup
        self.createActions()
        self.createMenus()

        # Done
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

    def createCallback(self, index: int):
        return lambda: self.enlarge(index)

    def displayThumbnails(self, layout):
        """Display grid of thumbnails."""
        cols = int((self.width - 150) / (1.25 * thumbnail_size.width()))
        rows = int((self.height - 150) / (1.25 * thumbnail_size.height()))

        self.search_fids = list(lb.search(None)) # Empty search = return all images
        if len(self.search_fids) > 16:
            self.search_fids = random.sample(self.search_fids, 16)

        self.search_results = [QPixmap('data/' + f) for f in self.search_fids]
        self.search_thumbs = [self.scaleImg(p, thumbnail_size) for p in self.search_results]

        # Dummy image
        #pixmap = self.scaleImg(QPixmap('image.png'), thumbnail_size)

        count = 0
        for i in range(rows):
            # Setting min size will make empty rows display
            layout.setColumnMinimumWidth(i, thumbnail_size.width())
            layout.setRowMinimumHeight(i, thumbnail_size.height())
            for j in range(cols):
                if (count < len(self.search_results)):
                    thumb = QExt.ImgButton(pixmap=self.search_thumbs[count])
                    # We require the createCallback() function to create a new
                    # scope so that the associated value of count is saved.
                    thumb.clicked.connect(self.createCallback(count))
                else:
                    thumb = QLabel()
                    thumb.hide()

                layout.addWidget(thumb, i, j)
                count += 1


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

    def enlarge(self, index: int):
        """Enlarge the search result thumbnail image."""
        print(index)
        self.imBox.hide()

        self.imageLabel.setPixmap(self.search_results[index])
        self.scaleFactor = 1.0
        self.fitToWindowAct.setEnabled(True)
        self.imZoomBox.show()

    def unenlarge(self):
        """Shrink the focused image and return to search results."""
        self.imZoomBox.hide()
        self.fitToWindowAct.setEnabled(False)
        self.imBox.show()



    #---------------------------------------------------------------------------
    # Image stuff
    #---------------------------------------------------------------------------
    def createActions(self):
#        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
#        self.printAct = QAction("&Print...", self, shortcut="Ctrl+P", enabled=False, triggered=self.print_)
#        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F",
                                      triggered=self.fitToWindow)
#        self.aboutAct = QAction("&About", self, triggered=self.about)
#        self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)

    def createMenus(self):
#        self.fileMenu = QMenu("&File", self)
#        self.fileMenu.addAction(self.openAct)
#        self.fileMenu.addAction(self.printAct)
#        self.fileMenu.addSeparator()
#        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

#        self.helpMenu = QMenu("&Help", self)
#        self.helpMenu.addAction(self.aboutAct)
#        self.helpMenu.addAction(self.aboutQtAct)

#        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
#        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        """Resize image to fit in the display area while maintaining the
        aspect ratio.
        """
        fitToWindow = self.fitToWindowAct.isChecked()
        if fitToWindow:
            bh, bw = self.imZoomBox.size().height(), self.imZoomBox.size().width()
            ih, iw = self.imageLabel.size().height(), self.imageLabel.size().width()
            hscale = bh / ih
            wscale = bw / iw
            if hscale < wscale:
                self.scaleImage(hscale)
            else:
                self.scaleImage(wscale)
        else:
            self.normalSize()

        self.updateActions()

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    lbm = LBmain(app)
    sys.exit(app.exec_())
