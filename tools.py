from PyQt5.QtWidgets import (QMenuBar, QToolBar, QFileDialog, QColorDialog,
                            QFontDialog, QInputDialog, QGraphicsItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from files import Files
from undo import *

class Toolbox(QToolBar):
    '''
    Sisältää piirtotyökalut
    '''
    def __init__(self, piirtoalusta):
        super().__init__()
        self.initUI()
        self.piirtoalusta = piirtoalusta

    def initUI(self):
        self.setMovable(False)
        self.addAction('Valinta', self.buttonClicked)
        self.addAction('Viiva', self.buttonClicked)
        self.addAction('Ellipsi', self.buttonClicked)
        self.addAction('Ympyrä', self.buttonClicked)
        self.addAction('Nelikulmio', self.buttonClicked)
        self.addAction('Teksti', self.buttonClicked)
        self.addSeparator()
        self.show()

    def buttonClicked(self):
        sender = self.sender()
        self.piirtoalusta.tool = sender.text()


class Colorbox(QToolBar):
    '''
    Sisältää värivalinta painikkeet
    '''
    def __init__(self, piirtoalusta):
        super().__init__()
        self.initUI()
        self.piirtoalusta = piirtoalusta

    def initUI(self):
        self.color = {'Musta': Qt.black, 'Sininen': Qt.blue, 'Punainen': Qt.red,
                        'Keltainen': Qt.yellow, 'Vihreä': Qt.green}
        self.setMovable(False)
        for key in self.color:
            self.addAction(key, self.buttonClicked)
        self.show()

    def buttonClicked(self):
        sender = self.sender()
        newcolor = self.color[sender.text()]
        selectedItems = self.piirtoalusta.scene.selectedItems()
        command = CommandColor(self.piirtoalusta.draw, selectedItems, newcolor)
        self.piirtoalusta.undoStack.push(command)


class Menubar(QMenuBar):
    '''
    Lisää painikkeita ja toimintoja menupalkkiin
    '''
    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        self.piirtoalusta = self.mainwindow.piirtoalusta
        self.undo = self.mainwindow.piirtoalusta.undoStack
        self.files = Files(self.piirtoalusta)
        self.setNativeMenuBar(False)
        filemenu = self.addMenu('File')
        editmenu = self.addMenu('Edit')
        filemenu.addAction('New', self.new)
        filemenu.addAction('Load', self.files.loadFile)
        filemenu.addAction('Save', self.files.saveFile)
        filemenu.addAction('Clear', self.clear)
        filemenu.addAction('Undo', self.undo.undo)
        editmenu.addAction('Delete', self.delete)
        editmenu.addAction('Color', self.color)
        editmenu.addAction('Font', self.font)
        editmenu.addAction('Group', self.group)
        editmenu.addAction('UnGroup', self.ungroup)
        self.show()

    def new(self):
        '''
        Luo uuden pääikkunan
        '''
        self.mainwindow.new()

    def clear(self):
        '''
        Poistaa kaikki esineet scenestä
        '''
        items = self.piirtoalusta.scene.items()
        command = CommandDelete(self.piirtoalusta.scene, items)
        self.piirtoalusta.undoStack.push(command)

    def color(self):
        '''
        Avaa väri-ikkunan värin valitsemiseen
        '''
        dialog = QColorDialog()
        newcolor = dialog.getColor()
        selectedItems = self.piirtoalusta.scene.selectedItems()
        command = CommandColor(self.piirtoalusta.draw, selectedItems, newcolor)
        self.piirtoalusta.undoStack.push(command)

    def font(self):
        '''
        Avaa Fontti-ikkunan fontin valintaan
        '''
        dialog = QFontDialog()
        dialog.setOption(QFontDialog.DontUseNativeDialog)
        newfont = dialog.getFont()[0]
        for item in self.piirtoalusta.scene.selectedItems():
            if item.type() == 8:
                command = CommandFont(self.piirtoalusta.draw, item, newfont)
                self.piirtoalusta.undoStack.push(command)
        self.piirtoalusta.draw.font = newfont

    def delete(self):
        '''
        Poistaa valitut esineet ja/tai ryhmät
        '''
        selectedItems = self.piirtoalusta.scene.selectedItems()
        command = CommandDelete(self.piirtoalusta.scene, selectedItems)
        self.piirtoalusta.undoStack.push(command)

    def group(self):
        '''
        Luo ryhmän valituista esineistä
        '''
        selectedItems = self.piirtoalusta.scene.selectedItems()
        self.piirtoalusta.scene.clearSelection()
        command = CommandGroup(self.piirtoalusta.scene, selectedItems)
        self.piirtoalusta.undoStack.push(command)

    def ungroup(self):
        '''
        Hajoittaa valitun ryhmän. Esineitä ei poisteta.
        '''
        for item in self.piirtoalusta.scene.selectedItems():
            command = CommandUnGroup(self.piirtoalusta.scene, item)
            self.piirtoalusta.undoStack.push(command)
