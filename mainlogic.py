from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import sqlite3 
from IndividInterface import Ui_Form as main_interface #Импорт интерфейса
from IndividDobavRedakt import Ui_Dialog as partner_interface
class partner_window (QDialog): #Класс главного окна добавления/редактирования
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = partner_interface()
        self.ui.setupUi(self)

        
        
    
        

        
class main_window (QWidget): #Класс главного окна программы
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = main_interface()
        self.ui.setupUi(self)
        self.read_partners()
        self.ui.pushButton.clicked.connect(self.open_add)
        self.ui.tableWidget.itemClicked.connect(self.open_update)
    def open_add(self):
        self.partner_form = partner_window(self)
        self.partner_form.exec()
    def open_update(self):
        current_row = self.ui.tableWidget.currentRow()
        if current_row >= 0 and current_row < len(self.books_data):
            self.partner_form = partner_window(self)
            books_data = self.books_data[current_row]
            self.partner_form.inn = books_data[0]  # id книги
            # Заполняем поля данными из выбранной книги
            self.partner_form.ui.lineEdit.setText(str(books_data[1]))  # Название
            self.partner_form.ui.lineEdit_2.setText(str(books_data[2]))  # Издательство
            self.partner_form.ui.lineEdit_3.setText(str(books_data[3]))  # Автор
            self.partner_form.ui.lineEdit_4.setText(str(books_data[4]))  # Год издания
            self.partner_form.ui.lineEdit_5.setText(str(books_data[5]))  # Цена
            
            self.partner_form.exec_()   
    def read_partners(self):
        self.ui.tableWidget.setRowCount(0)
        cursor.execute('SELECT * FROM Книги')
        self.books_data = cursor.fetchall()
        cursor.execute('SELECT idКниги, SUM(Количество) as total_count FROM Заказики GROUP BY idКниги ')
        self.orders_data  = {i[0]: i[1] for i in cursor.fetchall()}

        self.ui.tableWidget.setRowCount(len(self.books_data))
        
        self.ui.tableWidget.setColumnCount(2)
        for row in range(len(self.books_data)):
             # Формируем текст для первой колонки
            text = (self.books_data[row][1] + ' | ' + self.books_data[row][2]# Название | Издательство
                    + '\n' + self.books_data[row][3] # Автор
                    + '\n + Год: ' + self.books_data[row][4] + '\nЦена: ' # Год издания
                    + str(self.books_data[row][5])+ ' руб.')
            item = QTableWidgetItem()
            item.setText(text)
            self.ui.tableWidget.setItem(row,0,item)
            item = QTableWidgetItem()
            # Получаем общее количество заказов для текущей книги
            total_orders = self.orders_data.get(self.books_data[row][0], 0)
            if total_orders < 10000:
                item.setText('0%')
            elif total_orders >= 10000 and total_orders < 50000:
                item.setText('5%')
            elif total_orders >= 50000 and total_orders < 300000:
                item.setText('10%')
            else:
                item.setText('15%')
            self.ui.tableWidget.setHorizontalHeaderLabels(['Информация о книге', 'Скидка'])
            self.ui.tableWidget.horizontalHeader().setVisible(True)  # Показываем заголовки    
            self.ui.tableWidget.setItem(row,1,item)
QApplication.setStyle(QStyleFactory.create("Fusion"))#Выбор стиля
pal = QApplication.palette()

pal.setColor(QPalette.Window, QColor('#FFFFFF'))#Цвет основного фона
pal.setColor(QPalette.Window, QColor('#67BA80')) #Цвет доп фона
pal.setColor(QPalette.Window, QColor('#F4E8D3')) #Цвет акцентирования внимания
QApplication.setPalette(pal)

font = QFont('Segoe UI', 12) #Установка созданной палитры
QApplication.setFont(font)

conn = sqlite3.connect('knigi') #подключение к БД
cursor = conn.cursor() #создание объекта курсора 
app = QApplication(sys.argv)#создание объекта главного окна
 
main_form = main_window()
main_form.show()#вывод главного окна
sys.exit(app.exec_())
cursor.close()
conn.close()
