# Main GUI module for LocalBooru.
# Katerina R, July 2020

import sys
from collections import namedtuple
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
import random

import LocalBooru as lb
import LBQtExtensions as QExt

thumbnail_size = QtCore.QSize(240, 240)
thumbnail_padding_factor = 1.12
tag_width = 250
icon_path = './basic-ui-icons/SVGs/'
menu_icon_size = QtCore.QSize(64, 64)



class LBmain(QMainWindow):
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
        self.tagList.itemClicked.connect(self.onTagClick)

        self.tagEditButton = QPushButton('Edit Tags')
        self.tagEditButton.clicked.connect(self.onTagEditBut)

        tagLayout = QVBoxLayout()
        tagLayout.addWidget(self.tagList, QtCore.Qt.MinimumSize)
        tagLayout.addWidget(self.tagEditButton, QtCore.Qt.MinimumSize)
        self.tagBox.setLayout(tagLayout)

        # Create image display grid widget + layout:
        self.imBox = QGroupBox('Images')
        self.imLayout = QGridLayout()
        search_fids = list(lb.search(None)) # Empty search = return all images
        self.displayThumbnails(self.imLayout, search_fids)
        self.imBox.setLayout(self.imLayout)

        # Create image zoom display
        self.imZoomBox = QGroupBox('Image')
        self.imZoomLayout = QVBoxLayout(alignment=QtCore.Qt.AlignCenter)

        self.imageLabel = QExt.ImageLabel(onClick=self.unenlarge)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.imageLabel)

        self.imZoomLayout.addWidget(self.scrollArea)
        self.imZoomLayout.setSizeConstraint(QLayout.SetNoConstraint)
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
        search_but.clicked.connect(self.onSearchBut)

        # Add to topbar
        self.topbarLayout.addWidget(add_but)
        self.topbarLayout.addWidget(share_but)
        self.topbarLayout.addWidget(delete_but)
        self.topbarLayout.addWidget(self.search_query)
        self.topbarLayout.addWidget(search_but)

        self.topbarLayout.setAlignment(QtCore.Qt.AlignVCenter)

    @QtCore.pyqtSlot(QListWidgetItem)
    def onTagClick(self, item):
        """Action when an item in the list is clicked.

        Usage: listWidget.itemClicked.connect(TagList.Clicked)
        """
        # Lazy hack
        args = ['-S', item.text()]
        search_fids = list(lb.main(args))

        self.displayThumbnails(self.imLayout, search_fids)
        self.search_query.setText(item.text())
        # Do unenlarge() last bc it clears self.tagList
        self.unenlarge()

    def scaleImg(self, pix: QPixmap, size: QtCore.QSize):
        """Scale an a QPixmap and maintain aspect ratio."""
        return pix.scaled(size.width(), size.height(),
                QtCore.Qt.KeepAspectRatio,
                transformMode=QtCore.Qt.SmoothTransformation)

    def createCallback(self, index: int):
        return lambda: self.enlarge(index)

    # TODO possible memory leak here not deleting old QPixmaps when updating?
    def displayThumbnails(self, layout, search_fids):
        """Display grid of thumbnails."""
        cols = int((self.width - tag_width) / (thumbnail_padding_factor * thumbnail_size.width()))
        rows = int((self.height - tag_width) / (thumbnail_padding_factor * thumbnail_size.height()))
        n_pic = cols * rows

        self.search_fids = search_fids
        if len(self.search_fids) > n_pic:
            self.search_fids = random.sample(self.search_fids, n_pic)

        self.search_results = [QPixmap('data/' + f) for f in self.search_fids]
        self.search_thumbs = [self.scaleImg(p, thumbnail_size) for p in self.search_results]

        count = 0
        for i in range(rows):
            # Setting min size will make empty rows display
            layout.setColumnMinimumWidth(i, thumbnail_size.width())
            layout.setRowMinimumHeight(i, thumbnail_size.height())
            for j in range(cols):
                # Clear out any previous results
                if layout.itemAtPosition(i, j):
                    toRemove = layout.itemAtPosition(i, j).widget()
                    layout.removeWidget(toRemove)
                    toRemove.deleteLater()
                if (count < len(self.search_results)):
                    thumb = QExt.ImgButton(pixmap=self.search_thumbs[count])
                    # We require the createCallback() function to create a new
                    # scope so that the associated value of count is saved.
                    thumb.clicked.connect(self.createCallback(count))
                else:
                    thumb = QLabel()
                    thumb.hide()

                layout.addWidget(thumb, i, j, alignment=QtCore.Qt.AlignCenter)
                count += 1



    #---------------------------------------------------------------------------
    # Update functions
    #---------------------------------------------------------------------------




    #---------------------------------------------------------------------------
    # Button functions
    #---------------------------------------------------------------------------

    def add_dialogue(self):
        """Begin dialogue to add an image to the database."""
        filenames, _ = QFileDialog.getOpenFileNames(
            self, caption='Add Image',
            filter='Image Files (*.png *.jpg *.bmp)'
        )


        # Parse inputs if file(s) selected
        if len(filenames) > 0:
            inputParser = QExt.AddFileDialog(self, len(filenames)>1)
            tags = []
            if inputParser.exec():
                tags = inputParser.getFileParams()

            # Only add file if given at least one tag
            if tags:
                for filename in filenames:
                    args = ['-A', filename] + tags
                    lb.main(args) # Actually make library call to add the file
            else:
                alert = QMessageBox()
                alert.setText('Cannot add un-tagged image(s)!')
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

    def onSearchBut(self):
        """Perform a database search."""
        # Lazy hack
        if self.search_query.text():
            args = ['-S'] + self.search_query.text().split()
        else:
            args = ['-S']
        search_fids = list(lb.main(args))

        self.displayThumbnails(self.imLayout, search_fids)

    def onTagEditBut(self):
        """Edit tags for the selected image."""
        old_tags = self.tagList.list_of_tags
        tagUpdater = QExt.EditTagDialog(tags=old_tags, parent=self)
        if tagUpdater.exec_():
            old_tags = set(old_tags)
            updated_tags = tagUpdater.getUpdatedTags()

            if updated_tags != old_tags:
                lb.update_tags(self.current_fid, updated_tags)
                self.tagList.clear()
                # Remember: sort() is in place and returns nothing, so you
                # can't put list(updated_tags).sort() inside the call to
                # taglist.updateTags() bc it will operate on the null return
                # value.
                updated_tags = list(updated_tags)
                updated_tags.sort()
                self.tagList.updateTags(updated_tags)
                self.tagList.show()


    def enlarge(self, index: int):
        """Enlarge the search result thumbnail image."""
        self.imBox.hide()
        self.imZoomBox.show()
        self.imageLabel.setPixmap(self.search_results[index])
        self.current_fid = self.search_fids[index]
        # Remember: sort() is in place and returns nothing, so you can't put
        # list(lb.get_tags(...)).sort() inside the call to taglist.updateTags()
        # bc it will operate on the null return value.
        file_tags = list(lb.get_tags([self.current_fid]))
        file_tags.sort()
        self.tagList.updateTags(file_tags)
        self.scaleFactor = 1.0

        # Hack to make starting fitted to window work
        self.normalSize()
        self.fitToWindow()

    def unenlarge(self):
        """Shrink the focused image and return to search results."""
        self.tagList.clear()
        self.imZoomBox.hide()
        self.imBox.show()



    #---------------------------------------------------------------------------
    # Image stuff
    #---------------------------------------------------------------------------

    def createActions(self):
        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=True, triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=True, triggered=self.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=True, triggered=self.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=True, checkable=True, shortcut="Ctrl+F",
                                      triggered=self.fitToWindow)

    def createMenus(self):
        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.menuBar().addMenu(self.viewMenu)

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        """Resize image to fit in the display area while maintaining the aspect
        ratio.
        """
        bh, bw = self.scrollArea.size().height(), self.scrollArea.size().width()
        ih, iw = self.imageLabel.size().height(), self.imageLabel.size().width()
        hscale = bh / ih
        wscale = bw / iw
        if hscale < wscale:
            self.scaleImage(hscale)
        else:
            self.scaleImage(wscale)

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 4.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.25)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value() + ((factor - 1) * scrollBar.pageStep() / 2)))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    lbm = LBmain(app)
    sys.exit(app.exec_())