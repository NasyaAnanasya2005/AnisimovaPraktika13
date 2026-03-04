from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import sqlite3 
from IndividInterface import Ui_Form as main_interface #Импорт интерфейса

class main_window (QWidget): #Класс главного окна программы
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = main_interface()
        self.ui.setupUi(self)
        
conn = sqlite3.connect('knigi.db') #подключение к БД
cursor = conn.cursor() #создание объекта курсора 
main_form = main_window()#создание объекта главного окна
 
main_form.show()#вывод главного окна
sys.exit(app.exec_())
cursor.close()
conn.close()
