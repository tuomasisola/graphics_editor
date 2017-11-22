from PyQt5.QtWidgets import QUndoCommand, QGraphicsItem

'''
Undo ominaisuuden saavat komennot käytetään QUndoCommand luokkien kautta. Osassa
toiminnoissa olisi myös valmiina Redo vaihtoehto, mutta ominasuutta ei ole
ohjelmassa
'''

class CommandDraw(QUndoCommand):
    def __init__(self, scene, item):
        super(CommandDraw, self).__init__()
        self.item = item
        self.scene = scene

    def undo(self):
        self.scene.removeItem(self.item)


class CommandColor(QUndoCommand):
    def __init__(self, draw, selectedItems, newcolor):
        super(CommandColor, self).__init__()
        self.selectedItems = selectedItems
        self.draw = draw
        self.oldcolor = self.draw.color
        self.newcolor = newcolor

    def redo(self):
        self.draw.color = self.newcolor
        self.draw.change_selected_color(self.selectedItems)

    def undo(self):
        self.draw.color = self.oldcolor
        self.draw.change_selected_color(self.selectedItems)


class CommandFont(QUndoCommand):
    def __init__(self, draw, item, newfont):
        super(CommandFont, self).__init__()
        self.item = item
        self.draw = draw
        self.oldfont = self.draw.font
        self.newfont = newfont

    def redo(self):
        self.draw.font = self.newfont
        self.item.setFont(self.newfont)

    def undo(self):
        self.draw.font = self.oldfont
        self.item.setFont(self.draw.font)


class CommandDelete(QUndoCommand):
    def __init__(self, scene, items):
        super(CommandDelete, self).__init__()
        self.items = items
        self.scene = scene

    def redo(self):
        for item in self.items:
            self.scene.removeItem(item)

    def undo(self):
        for item in self.items:
            self.scene.addItem(item)


class CommandGroup(QUndoCommand):
    def __init__(self, scene, items):
        super(CommandGroup, self).__init__()
        self.items = items
        self.scene = scene

    def redo(self):
        self.newgroup = self.scene.createItemGroup(self.items)
        self.newgroup.setFlag(QGraphicsItem.ItemIsSelectable)
        self.newgroup.setFlag(QGraphicsItem.ItemIsMovable)

    def undo(self):
        self.scene.destroyItemGroup(self.newgroup)


class CommandUnGroup(QUndoCommand):
    def __init__(self, scene, group):
        super(CommandUnGroup, self).__init__()
        self.group = group
        self.scene = scene
        self.items = self.group.childItems()

    def redo(self):
        self.scene.destroyItemGroup(self.group)

    def undo(self):
        self.piirtoalusta.scene.clearSelection()
        self.newgroup = self.scene.createItemGroup(self.items)
        self.newgroup.setFlag(QGraphicsItem.ItemIsSelectable)
        self.newgroup.setFlag(QGraphicsItem.ItemIsMovable)


class CommandClear(QUndoCommand):
    def __init__(self, scene, items):
        super(CommandClear, self).__init__()
        self.items = items
        self.scene = scene

    def redo(self):
        for item in self.items:
            self.scene.removeItem(item)

    def undo(self):
        for item in self.items:
            self.scene.addItem(item)


class CommandMove(QUndoCommand):
    def __init__(self, old, item):
        super(CommandMove, self).__init__()
        self.item = item
        self.old = old

    def undo(self):
        self.item.setPos(self.old)
