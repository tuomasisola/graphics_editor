from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsPathItem, QGraphicsTextItem

from undo import CommandMove

'''
Nämä Esine-luokat on uudelleen määritetty, jotta voidaan pitää kirjaa niiden
liikuttamisesta Undo luokkaa varten.
'''

class EllipseItem(QGraphicsEllipseItem):
    def __init__(self, rect, undoStack):
        super(EllipseItem, self).__init__(rect)
        self.oldpos = None
        self.newpos = None
        self.undoStack = undoStack

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.oldpos = self.pos()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.pos() != self.oldpos:
            command = CommandMove(self.oldpos, self)
            self.undoStack.push(command)


class PathItem(QGraphicsPathItem):
    def __init__(self, rect, undoStack):
        super(PathItem, self).__init__(rect)
        self.oldpos = None
        self.newpos = None
        self.undoStack = undoStack

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.oldpos = self.pos()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.pos() != self.oldpos:
            command = CommandMove(self.oldpos, self)
            self.undoStack.push(command)


class TextItem(QGraphicsTextItem):
    def __init__(self, rect, undoStack):
        super(TextItem, self).__init__(rect)
        self.oldpos = None
        self.newpos = None
        self.undoStack = undoStack

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.oldpos = self.pos()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.pos() != self.oldpos:
            command = CommandMove(self.oldpos, self)
            self.undoStack.push(command)
