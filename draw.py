from PyQt5.QtWidgets import (QGraphicsEllipseItem, QGraphicsRectItem,
                            QGraphicsPathItem, QGraphicsTextItem, QGraphicsItem)
from PyQt5.QtCore import QRectF, Qt, QPoint
from PyQt5.QtGui import QPainterPath, QPen, QFont

from undo import *
from items import *


class DrawItem():
    '''
    Piirtää kuviot
    '''
    def __init__(self, piirtoalusta):
        self.scene = piirtoalusta.scene
        self.undoStack = piirtoalusta.undoStack
        self.reset()
        self.start = QPoint()
        self.end = QPoint()
        self.pos = QPoint()
        self.color = Qt.black
        self.font = QFont()

    def setRect(self):
        '''
        Määrittää nelikulmion paikkatietojen perusteella
        '''
        rect = QRectF()
        rect.setTopLeft(self.start)
        rect.setBottomRight(self.end)
        return rect

    def drawRect(self):
        '''
        Piirtää esineen ja lisää sen sceneen. Palauttaa esineen Load ja
        Undo luokkia varten.
        '''
        path = QPainterPath()
        rect = self.setRect()
        path.addRect(rect)
        path.simplified()
        #self.rectitem = QGraphicsPathItem(path)
        self.rectitem = PathItem(path, self.undoStack)
        self.rectitem.setPen(QPen(self.color, 2))
        self.rectitem.setFlag(QGraphicsItem.ItemIsSelectable)
        self.rectitem.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(self.rectitem)
        return self.rectitem
        '''
        rect = self.setRect()
        self.rectitem = QGraphicsRectItem(rect)
        self.rectitem.setPen(QPen(self.color, 2))
        self.scene.addItem(self.rectitem)
        '''

    def drawEllipse(self):
        rect = self.setRect()
        #self.ellipseitem = QGraphicsEllipseItem(rect)
        self.ellipseitem = EllipseItem(rect, self.undoStack)
        self.ellipseitem.setPen(QPen(self.color, 2))
        self.ellipseitem.setFlag(QGraphicsItem.ItemIsSelectable)
        self.ellipseitem.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(self.ellipseitem)
        return self.ellipseitem

    def drawCircle(self):
        erotus = abs(self.end.x() - self.start.x())
        if self.start.y() > self.end.y():
            erotus = -erotus
        self.end.setY(self.start.y() + erotus)
        self.drawEllipse()

    def drawLine(self):
        path = QPainterPath()
        shape = QRectF(0,0,1,1)
        shape.moveCenter(self.pos)
        path.addEllipse(shape)
        self.paths.connectPath(path)
        self.paths.simplified()
        #self.lineitem = QGraphicsPathItem(self.paths)
        self.lineitem = PathItem(self.paths, self.undoStack)
        self.lineitem.setPen(QPen(self.color, 2))
        self.lineitem.setFlag(QGraphicsItem.ItemIsSelectable)
        self.lineitem.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(self.lineitem)
        return self.lineitem

    def drawText(self):
        #textitem = QGraphicsTextItem('Text')
        textitem = TextItem('Text', self.undoStack)
        textitem.setPos(self.end)
        textitem.setAcceptHoverEvents(False)
        textitem.setTextInteractionFlags(Qt.TextSelectableByKeyboard | Qt.TextEditable)
        textitem.setFont(self.font)
        textitem.setDefaultTextColor(self.color)
        textitem.setFlag(QGraphicsItem.ItemIsMovable)
        textitem.setFlag(QGraphicsItem.ItemIsSelectable)
        self.scene.addItem(textitem)
        return textitem

    def reset(self):
        self.ellipseitem = QGraphicsEllipseItem()
        self.rectitem = QGraphicsRectItem()
        self.lineitem = QGraphicsPathItem()
        self.paths = QPainterPath()

    def change_selected_color(self, items):
        '''
        Muttaa listan 'items' esineiden värin arvoon 'self.color'.
        '''
        for item in items:
            if item.type() == 10:                                       # group
                self.change_selected_color(item.childItems())           # kutsuu itseään joukon jäsenille
            elif item.type() == 8:                                      # tekstiä
                item.setDefaultTextColor(self.color)
            else:
                item.setPen(QPen(self.color, 2))
