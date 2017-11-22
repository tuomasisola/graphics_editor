import sys
from PyQt5.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView,
                            QMainWindow, QUndoStack)
from PyQt5.QtCore import Qt
from draw import DrawItem
from tools import Toolbox, Menubar, Colorbox
from undo import *


class MainWindow(QMainWindow):
    '''
    Luo pääikkunan ja lisää siihen piirustusalustan ja työkalupalkit
    '''
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.piirtoalusta = Piirtoalusta()
        toolbox = Toolbox(self.piirtoalusta)
        colorbox = Colorbox(self.piirtoalusta)
        self.menubar = Menubar(self)
        self.setMenuBar(self.menubar)
        self.addToolBar(Qt.LeftToolBarArea, toolbox)
        self.addToolBar(Qt.LeftToolBarArea, colorbox)
        self.setCentralWidget(self.piirtoalusta)
        self.setWindowTitle('YoloPaint')
        self.show()

    def new(self):
        '''
        Luo toisen pääikkunan
        '''
        self.newwindow = MainWindow()


class Piirtoalusta(QGraphicsView):
    '''
    Hallitsee Scenenä mihin piirretään. Huolehtii myös hiiren tapahtumien
    nappaamisesta ja eteenpäin ohjaamisesta.
    '''
    def __init__(self):
        super().__init__()
        self.undoStack = QUndoStack(self)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 500, 500)
        self.setScene(self.scene)
        self.tool = 'Valinta'
        self.show()
        self.draw = DrawItem(self)

    def mouseMoveEvent(self, event):
        '''
        Tarkistaa käytetäänkö hiiren perustoimintoa vai ollaanko piirtämässä.
        '''
        if self.tool == 'Valinta':
            super().mouseMoveEvent(event)
        else:
            self.mouseMove(event)

    def mousePressEvent(self, event):
        if self.tool == 'Valinta':
            super().mousePressEvent(event)
        else:
            self.mousePress(event)

    def mouseReleaseEvent(self, event):
        if self.tool == 'Valinta':
            super().mouseReleaseEvent(event)
        else:
            self.mouseRelease(event)

    def mouseMove(self, event):
        '''
        Uudelleen määritelty mouseMoveEvent. Tarkistaa mikä työkalu on käytössä
        ja piirtää oikeaa kuviota jos hiiren nappi on pohjassa
        '''
        self.draw.pos = event.pos()
        if self.tool == 'Viiva':
            if self.draw.lineitem.isActive():
               self.scene.removeItem(self.draw.lineitem)
            self.draw.drawLine()
        elif self.tool == 'Nelikulmio':
            if self.draw.rectitem.isActive():
               self.scene.removeItem(self.draw.rectitem)
            self.draw.end = event.pos()
            item = self.draw.drawRect()
        elif self.tool == 'Ellipsi':
            if self.draw.ellipseitem.isActive():
                self.scene.removeItem(self.draw.ellipseitem)
            self.draw.end = event.pos()
            self.draw.drawEllipse()
        elif self.tool == 'Ympyrä':
            if self.draw.ellipseitem.isActive():
                self.scene.removeItem(self.draw.ellipseitem)
            self.draw.end = event.pos()
            self.draw.drawCircle()

    def mousePress(self, event):
        '''
        Nappaa kohdan jossa hiiren nappi painetaan alas
        '''
        self.draw.start = event.pos()

    def mouseRelease(self, event):
        '''
        Nappaa kohdan, jossa hiiren napista päästetään irti. Välittää piirretyn
        esineen Undo-luokalle.
        '''
        self.draw.end = event.pos()
        if self.tool == 'Nelikulmio':
            command = CommandDraw(self.scene, self.draw.rectitem)
            self.undoStack.push(command)
        elif self.tool == 'Ellipsi' or self.tool == 'Ympyrä':
            command = CommandDraw(self.scene, self.draw.ellipseitem)
            self.undoStack.push(command)
        elif self.tool == 'Viiva':
            command = CommandDraw(self.scene, self.draw.lineitem)
            self.undoStack.push(command)
        elif self.tool == 'Teksti':
            textitem = self.draw.drawText()
            self.tool = 'Valinta'
            command = CommandDraw(self.scene, textitem)
            self.undoStack.push(command)
        self.draw.reset()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
