from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsItem

class Load():
    '''
    Ottaa tekstitiedoston 'input_file', ja lataa tiedoston mukaiset esineet sceneen
    '''
    def __init__(self, input_file, piirtoalusta):
        self.piirtoalusta = piirtoalusta
        self.groups = {}
        for l in input_file:
            line = l.split('<value>')
            if line[0] == 'Ellipse':
                self.ellipse(line)
            elif line[0] == 'Rect':
                self.rect(line)
            elif line[0] == 'Line':
                self.line(line)
            elif line[0] == 'Text':
                self.text(line)
            else:
                raise TypeError("Unidentified shape {}".format(line[0]))

    def ellipse(self, line):
        self.points(line)
        item = self.piirtoalusta.draw.drawEllipse()
        self.addToGroup(item, line[6])

    def rect(self, line):
        self.points(line)
        item = self.piirtoalusta.draw.drawRect()
        self.addToGroup(item, line[6])

    def line(self,line):
        item = None
        points = line[1].split(';')
        self.piirtoalusta.draw.color = QColor(int(line[2]))
        for point in points:
            if item is not None:
                self.piirtoalusta.scene.removeItem(item)
            xy = point.split(':')
            self.piirtoalusta.draw.pos.setX(int(xy[0]))
            self.piirtoalusta.draw.pos.setY(int(xy[1]))
            item = self.piirtoalusta.draw.drawLine()
        self.addToGroup(item, line[3])
        self.piirtoalusta.draw.reset()
        item = None

    def text(self,line):
        '''
        Tallenteeseen muutetaan '\n' ja ':' merkit takaisin, jotta
        jotta teksti tulee esineeseen oikein
        '''
        self.piirtoalusta.draw.font.fromString(line[1])
        text = line[2]
        self.piirtoalusta.draw.end.setX(int(line[3]))
        self.piirtoalusta.draw.end.setY(int(line[4]))
        self.piirtoalusta.draw.color = QColor(int(line[5]))
        textitem = self.piirtoalusta.draw.drawText()
        text = text.replace('<br>', '\n')
        text = text.replace('<colon>', ':')
        textitem.setPlainText(text)
        self.addToGroup(textitem, line[6])

    def points(self, line):
        '''
        Määrittää sijainti- ja väritiedot luotavalle esineelle
        '''
        self.piirtoalusta.draw.start.setX(int(line[1]))
        self.piirtoalusta.draw.start.setY(int(line[2]))
        self.piirtoalusta.draw.end.setX(int(line[3]))
        self.piirtoalusta.draw.end.setY(int(line[4]))
        self.piirtoalusta.draw.color = QColor(int(line[5]))

    def addToGroup(self, item, name):
        '''
        Määrittää saman ryhmänimen omaaville yhteisen ryhmän ja palauttaa sen
        '''
        if name.strip() == 'None':
            return None
        elif name not in self.groups:
            group = QGraphicsItemGroup()
            self.piirtoalusta.scene.addItem(group)
            group.setFlag(QGraphicsItem.ItemIsSelectable)
            group.setFlag(QGraphicsItem.ItemIsMovable)
            group.addToGroup(item)
            self.groups.update({name:group})
        else:
            group = self.groups[name]
            group.addToGroup(item)
