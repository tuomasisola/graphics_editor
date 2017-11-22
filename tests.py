import unittest
import sys
from io import StringIO
from PyQt5.QtWidgets import QApplication

from piirustusohjelma import MainWindow
from load import Load


class Test(unittest.TestCase):
    '''
    Testaa lataus, tallennus, clear ja rikkinäinen tiedosto
    '''
    def test_load(self):
        self.input_file = StringIO()
        self.input_file.write('Text<value>.SF NS Text,13,-1,5,50,0,0,0,0,0<value>Text<value>48<value>218<value>4278190335<value>Group1\n')
        self.input_file.write('Ellipse<value>237<value>277<value>344<value>392<value>4278190335<value>Group1\n')
        self.input_file.write('Line<value>315:58;315:59;315:61;317:67;321:72;324:'
                                '76;332:93;342:108;351:117;357:124;360:129;365:'
                                '134;367:137;368:140;370:143;373:147;375:151;375:'
                                '152;376:152;377:156;377:157;377:158<value>'
                                '4294901760<value>Group2\n')
        self.input_file.write('Rect<value>176<value>131<value>92<value>50<value>4294901760<value>Group2\n')
        self.input_file.seek(0, 0)

        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        load = Load(self.input_file, mainwindow.piirtoalusta)
        self.input_file.close()
        items = mainwindow.piirtoalusta.scene.items()

        self.assertEqual(6 ,len(items),  "Loading data failed. Wrong number of items")


    def test_save(self):
        incontent = 'Text<value>.SF NS Text,13,-1,5,50,0,0,0,0,0<value>Text<value>48<value>218<value>4278190335<value>Group1\n'
        self.input_file = StringIO()
        self.input_file.write(incontent)
        self.input_file.seek(0, 0)

        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        load = Load(self.input_file, mainwindow.piirtoalusta)
        self.input_file.close()
        mainwindow.menubar.files.filename = '/Users/Tuomas/Python3/Y2-Piirustusohjelma/testi2.txt'
        outcontent = mainwindow.menubar.files.saveFile()

        self.assertEqual(incontent, outcontent,  "Loading data failed. Data does not match")

    '''
    def test_undo(self):
        self.input_file = StringIO()
        self.input_file.write('Line,75:91;74:91;74:90;75:90;123:134,4278190080\n')
        self.input_file.write('Rect,123,21,235,139,4294901760\n')
        self.input_file.write('Line,42:91;44:94;94:100;126:144,4278190081\n')
        self.input_file.write('Rect,153,31,335,138,4294901760\n')
        self.input_file.write('Ellipse,248,31,275,58,4278190335\n')
        self.input_file.write('Ellipse,62,44,142,90,4278190080\n')
        self.input_file.seek(0, 0)

        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.files.loadFile(self.input_file)
        self.input_file.close()
        old = mainwindow.piirtoalusta.scene.items()
        mainwindow.undo()
        new = mainwindow.piirtoalusta.scene.items()

        self.assertNotEqual(new[0] , old[0],  "Undo failed. Item still there")
    '''

    def test_clear(self):
        self.input_file = StringIO()
        self.input_file.write('Text<value>.SF NS Text,13,-1,5,50,0,0,0,0,0<value>Text<value>48<value>218<value>4278190335<value>Group1\n')
        self.input_file.write('Ellipse<value>237<value>277<value>344<value>392<value>4278190335<value>Group1\n')
        self.input_file.write('Line<value>315:58;315:59;315:61;317:67;321:72;324:'
                                '76;332:93;342:108;351:117;357:124;360:129;365:'
                                '134;367:137;368:140;370:143;373:147;375:151;375:'
                                '152;376:152;377:156;377:157;377:158<value>'
                                '4294901760<value>Group2\n')
        self.input_file.write('Rect<value>176<value>131<value>92<value>50<value>4294901760<value>Group2\n')
        self.input_file.seek(0, 0)

        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        load = Load(self.input_file, mainwindow.piirtoalusta)
        self.input_file.close()
        mainwindow.menubar.clear()
        items = mainwindow.piirtoalusta.scene.items()

        self.assertEqual(0 , len(items),  "Undo failed. Item still there")

    def test_broken_file(self):
        self.input_file = StringIO()
        self.input_file.write('Text<value>.SF NS Text,13,-1,5,50,0,0,0,0,0<value>Text<value>48<value>218<value>4278190335<value>Group1\n')
        self.input_file.write('Hupsu<value>237<value>277<value>344<value>392<value>4278190335<value>Group1\n')
        self.input_file.write('Line<value>315:58;315:59;315:61;317:67;321:72;324:'
                                '76;332:93;342:108;351:117;357:124;360:129;365:'
                                '134;367:137;368:140;370:143;373:147;375:151;375:'
                                '152;376:152;377:156;377:157;377:158<value>'
                                '4294901760<value>Group2\n')
        self.input_file.write('Rect<value>176<value>131<value>92<value>50<value>4294901760<value>Group2\n')
        self.input_file.seek(0, 0)

        app = QApplication(sys.argv)
        mainwindow = MainWindow()

        self.assertRaises(TypeError, Load, self.input_file, mainwindow.piirtoalusta)
        self.input_file.close()

    def close_silently(self,r):
        try:
            r.close()
        except OSError:
            ''' ignore'''


if __name__ == '__main__':
    unittest.main()
