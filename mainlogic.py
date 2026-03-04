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
        self.read_partners()

    def read_partners(self):
        self.ui.tableWidget.setRowCount(0)
        cursor.execute('SELECT * FROM Partners')
        self.partners_data = cursor.fetchall()
        cursor.execute('select id   ')
        self.skidka = {i[0]: i[1] for i in cursor.fetchall()}

        self.ui.tableWidget.setRowCount(len(self.partners_data))
        for row in range(len(self.partners_data)):
            text = (self.partners_data[row][1] + ' | ' + self.partners_data[row][2]
                    + '\n' + self.partners_data[row][3]
                    + '\n + 7 ' + self.partners_data[row][5] + '\nРейтинг: '
                    + str(self.partners_data[row][7]))
            item = QTableWidgetItem()
            item.setText(text)
            self.ui.tableWidget.setItem(row,0,item)
            item = QTableWidgetItem()
            if current_skidka == None:
                item.setText('0%')
            elif current_skidka < 10000:
                item.setText('0%')
            elif current_skidka >=10000 and current_skidka < 50000:
                item.setText('5%')
            elif current_skidka >= 50000 and current_skidka < 300000:
                item.setText('10%')
            else:
                item.setText('15%')
            self.ui.tableWidget.setItem(row,1,item)
QApplication.setStyle(QStyleFactory.create("Fusion"))#Выбор стиля
pal = QApplication.palette()

pal.setColor(QPalette.Window, QColor('#FFFFFF'))#Цвет основного фона
pal.setColor(QPalette.Window, QColor('#67BA80')) #Цвет доп фона
pal.setColor(QPalette.Window, QColor('#F4E8D3')) #Цвет акцентирования внимания
QApplication.setPalette(pal)

font = QFont('Segoe UI', 12) #Установка созданной палитры
QApplication.setFont(font)

conn = sqlite3.connect('knigi.db') #подключение к БД
cursor = conn.cursor() #создание объекта курсора 
app = QApplication(sys.argv)#создание объекта главного окна
 
main_form = main_window()
main_form.show()#вывод главного окна
sys.exit(app.exec_())
cursor.close()
conn.close()
