from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QSaveFile, QIODevice, QByteArray

from save import Save
from load import Load

class Files():
    '''
    Kommunikoi tallennuksen ja latauksen tiedostojen kanssa. Kysyy
    tiedostopolkua jos sitä ei ole ennestään annettu. Save ja Load -luokat
    hoitavat varinaiset item to string ja string to item muunnokset.
    '''
    def __init__(self, piirtoalusta):
        self.filename = ''
        self.piirtoalusta = piirtoalusta

    def saveFile(self):
        if self.filename is '':
            self.filename = QFileDialog.getSaveFileName(self.piirtoalusta)[0]
        if self.filename is not '':
            items = self.piirtoalusta.scene.items()
            if '.txt' not in self.filename:
                self.filename = "".join((self.filename, '.txt'))
            textfile = QSaveFile(self.filename)
            textfile.open(QIODevice.WriteOnly | QIODevice.Text)
            output = QByteArray()
            items = self.piirtoalusta.scene.items()
            save = Save(items)
            output.append(save.content)
            textfile.write(output)
            textfile.commit()
            return save.content

    def loadFile(self):
        input_file = None
        try:
            path = QFileDialog.getOpenFileName(self.piirtoalusta)[0]
            input_file = open(path)
        except OSError:
            print("Could not open {}".format(path))
        else:
            Load(input_file, self.piirtoalusta)
        finally:
            if input_file:
                input_file.close()
