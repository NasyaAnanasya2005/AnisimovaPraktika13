from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import sqlite3 
from IndividInterface import Ui_Form as main_interface #Импорт интерфейса
from IndividDobavRedakt import Ui_Dialog as partner_interface
from login import Ui_Dialog as login_interface


class loginWindow(QDialog): #окно логирования
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.ui = login_interface()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.disconnect()
        self.ui.buttonBox.accepted.connect(self.log)
        self.ui.buttonBox.rejected.connect(self.log_gost)
    def log(self): #функция входа
        log = "admin"
        pas = "admin123"
        login = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        if login == log and password == pas:
            QMessageBox.information(self, 'Информация', 'Вы успешно вошли', QMessageBox.Ok)
            self.accept() # Закрываем окно логина
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль!', QMessageBox.Ok)
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            self.ui.lineEdit.setFocus()
    def log_gost(self): #если пользователь нажал кнопку Отмена, то заходит как Гость
        QMessageBox.information(self, 'Информация', 'Вы предпочли уйти :(.', QMessageBox.Ok)
        self.reject() # Закрываем окно логина
class partner_window (QDialog): #Класс главного окна добавления/редактирования
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = partner_interface()
        self.ui.setupUi(self)
    def create_partner(self):
        partner_data = [
            self.ui.lineEdit.text(),  # Название
            self.ui.lineEdit_2.text(),  # Издательство
            self.ui.lineEdit_3.text(),  # Автор
            self.ui.lineEdit_4.text(),  # Год издания
            self.ui.lineEdit_5.text()  # Цена
        ]
        if any([item == ' ' for item in partner_data]): #Проверка на пустые значения
            QMessageBox.critical(self, 'Действие не выполнено',  'Заполните поля', QMessageBox.Ok)
            return
        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите добавить?', QMessageBox.Ok | QMessageBox.Cancel)
        if q == QMessageBox.Ok:
            try:
                cursor.execute("INSERT INTO Книги (Название, Издательство, Автор, \"Год издания\", Цена) VALUES (?,?,?,?,?)", partner_data)
                conn.commit()
                main_form.read_partners() #Обновление списка партнеров на главное окне
                QMessageBox.information(self, 'Действие выполнено' , 'Добавлен', QMessageBox.Ok)
                self.accept() #Закрытие диалоговое окна
                return
            except:
                QMessageBox.critical(self, 'Действие не выполнено', 'Ошибка добавления', QMessageBox.Ok)
    def update_partner(self):
        partner_data = [
            self.ui.lineEdit.text(),  # Название
            self.ui.lineEdit_2.text(),  # Издательство
            self.ui.lineEdit_3.text(),  # Автор
            self.ui.lineEdit_4.text(),  # Год издания
            self.ui.lineEdit_5.text()  # Цена
        ]
        if any([item == ' ' for item in partner_data[:-1]]): #Проверка на пустые значения
            QMessageBox.critical(self, 'Действие не выполнено',  'Заполните поля', QMessageBox.Ok)
            return
        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите изменить?', QMessageBox.Ok | QMessageBox.Cancel)
        if q == QMessageBox.Ok:
            try:
                # Получаем ID из родительского окна
                book_id = self.parent().books_data[self.parent().ui.tableWidget.currentRow()][0]
                cursor.execute("UPDATE Книги SET Название=?, Издательство=?, Автор=?, \"Год издания\"=?, Цена=? WHERE idКниги=?", partner_data + [book_id])
                conn.commit()
                main_form.read_partners() #Обновление списка партнеров на главное окне
                QMessageBox.information(self, 'Действие выполнено' , 'Изменено', QMessageBox.Ok)
                self.accept() #Закрытие диалоговое окна
                return
            except Exception as e:
                QMessageBox.critical(self, 'Действие не выполнено', f'Ошибка изменения: {str(e)}', QMessageBox.Ok)    
class main_window (QWidget): #Класс главного окна программы
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = main_interface()
        self.ui.setupUi(self)
        self.read_partners()
        self.ui.pushButton.clicked.connect(self.open_add)
        self.ui.tableWidget.itemDoubleClicked.connect(self.open_update)
        self.ui.pushButton_1.clicked.connect(self.dell)
    def dell(self): #удаление 
        r = self.ui.tableWidget.currentRow() #выбранная строка 
        if r == -1:
            QMessageBox.critical(self, 'Ошибка', 'Выберите книгу для удаления.', QMessageBox.Ok)
            return
        book_id = self.books_data[r][0]  # idКниги
        # Проверяем, есть ли заказы с этой книгой
        cursor.execute('SELECT COUNT(*) FROM Заказики  WHERE idКниги=?', [book_id])
        d = int(cursor.fetchone()[0])
        if d == 0: #если заказов нет, то удаляем
            try:
                cursor.execute('DELETE FROM Книги WHERE idКниги=?', [book_id])
                conn.commit()
                self.read_partners() #обновляем таблицу с книгами
                QMessageBox.information(self, 'Информация', 'Книга успешно удалена.', QMessageBox.Ok)
            except:
                QMessageBox.critical(self, 'Ошибка', 'Не удалось удалить.', QMessageBox.Ok)
        else:
            QMessageBox.critical(self, 'Ошибка', 'Эту книгу нельзя удалить, так как она есть в заказах.', QMessageBox.Ok)

    def open_add(self):
        self.partner_form = partner_window(self)
        self.partner_form.ui.buttonBox.accepted.connect(self.partner_form.create_partner)
        self.partner_form.exec_()
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
            self.partner_form.ui.buttonBox.accepted.connect(self.partner_form.update_partner)
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
 
# СОЗДАЕМ главное окно (НО НЕ ПОКАЗЫВАЕМ)
main_form = main_window()
# СОЗДАЕМ И ПОКАЗЫВАЕМ окно логина
login_form = loginWindow()
# Запускаем окно логина и проверяем результат
result = login_form.exec_()
# Если пользователь нажал OK (успешный вход как админ)
if result == QDialog.Accepted:
    main_form.show()
    sys.exit(app.exec_())
# Если пользователь нажал Cancel (вход как гость)
else:
    cursor.close()
    conn.close()
    sys.exit()

