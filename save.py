class Save():
    '''
    Ottaa listan 'items' esineistä ja muuntaa ne muotoon string 'self.content'.
    Huomaa että sijaintiin lisätään mahdollisen hiirellä tehdyn siirtämisen
    vaikutukset lisäämällä item.pos(), siirtäminen ei tallennu elementteihin.
    '''
    def __init__(self, items):
        self.lista = []
        self.groups = {}
        for item in items:
            if item.type() == 2:
                path = item.path()
                if path.elementCount() == 5:
                    self.rect(item, path)
                else:
                    self.line(item, path)
            elif item.type() == 4:
                self.ellipse(item)
            elif item.type() == 8:
                self.text(item)
        self.content = "\n".join(self.lista) + '\n'

    def rect(self, item, path):
        topLeftX = int(path.elementAt(2).x) + int(item.pos().x())
        # sijaintiin lisätään mahdollisen hiirellä tehdyn siirtämisen vaikutukset
        topLeftY = int(path.elementAt(2).y) + int(item.pos().y())
        bottomRightX = int(path.elementAt(4).x) + int(item.pos().x())
        bottomRightY = int(path.elementAt(4).y) + int(item.pos().y())
        color = item.pen().color().rgb()
        grouppointer = item.parentItem()
        groupname = self.groupname(grouppointer)
        self.lista.append("<value>".join(('Rect', str(topLeftX), str(topLeftY),
                                str(bottomRightX), str(bottomRightY),
                                str(color), groupname)))

    def line(self, item, path):
        positions = []
        for i in range(0, path.elementCount()):
            element = path.elementAt(i)
            if element.type == 1 or element.type == 0:
                posX = int(element.x) + int(item.pos().x())
                posY = int(element.y) + int(item.pos().y())
                positions.append(":".join((str(posX), str(posY))))
        color = item.pen().color().rgb()
        positions = ";".join(positions)
        grouppointer = item.parentItem()
        groupname = self.groupname(grouppointer)
        self.lista.append("<value>".join(('Line', positions, str(color), groupname)))

    def ellipse(self, item):
        rect = item.rect()
        topLeftX = int(rect.topLeft().x()) + int(item.pos().x())
        topLeftY = int(rect.topLeft().y()) + int(item.pos().y())
        bottomRightX = int(rect.bottomRight().x()) + int(item.pos().x())
        bottomRightY = int(rect.bottomRight().y()) + int(item.pos().y())
        color = item.pen().color().rgb()
        grouppointer = item.parentItem()
        groupname = self.groupname(grouppointer)
        self.lista.append("<value>".join(('Ellipse', str(topLeftX), str(topLeftY),
                                str(bottomRightX), str(bottomRightY),
                                str(color), groupname)))

    def text(self, item):
        '''
        Tallenteeseen muutetaan '\n' ja ':' merkit, jotta Load metodi toimii oikein
        '''
        font = item.font().toString()
        pos = item.pos()
        color = item.defaultTextColor().rgb()
        text = item.toPlainText()
        text = text.replace('\n', '<br>')
        text = text.replace(':', '<colon>')
        grouppointer = item.parentItem()
        groupname = self.groupname(grouppointer)
        self.lista.append("<value>".join(('Text', font, text, str(int(pos.x())),
                                str(int(pos.y())), str(color), groupname)))

    def groupname(self, pointer):
        '''
        Määrittää samalle ryhmälle yhteisen nimen Group1, Group2, ... , GroupN
        ja palauttaa nimen
        '''
        if pointer is None:
            return 'None'
        elif pointer not in self.groups:
            name = 'Group{}'.format(len(self.groups) + 1)
            self.groups.update({pointer:name})
        return self.groups[pointer]
