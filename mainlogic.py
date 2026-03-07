from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import sqlite3 
from IndividInterface import Ui_Form as main_interface #Импорт интерфейса
from IndividDobavRedakt import Ui_Dialog as partner_interface
from login import Ui_Dialog as login_interface
from menu import Ui_Form as menu_interface  # Импорт интерфейса меню
from IndividInterfaceOptBuy import Ui_Form as buyers_interface
from OptBuyDobavRedakt import Ui_Dialog as buyers_edit_interface
from IndividInterfaceZakaziki import Ui_Form as orders_interface  # Для заказов
from ZakazDobavRedakt import Ui_Dialog as orders_edit_interface
import os
import shutil
from PIL import Image
from PyQt5.QtGui import QIcon, QPixmap
class orders_window(QWidget):  # Окно со списком заказов
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = orders_interface()
        self.ui.setupUi(self)
        self.read_orders()
        self.ui.pushButton.clicked.connect(self.open_add)  # Добавить
        self.ui.pushButton_2.clicked.connect(self.dell)    # Удалить
        self.ui.tableWidget.itemDoubleClicked.connect(self.open_update)  # Редактировать
    
    def read_orders(self):
        #Чтение данных из таблицы Заказики с подстановкой названий
        self.ui.tableWidget.setRowCount(0)
        
        # Запрос с JOIN, чтобы получить названия книги и фирмы
        query = '''
        SELECT Заказики.*, Книги.Название, ОптовыеПокупатели.ФирмаПокупатель 
        FROM Заказики
        LEFT JOIN Книги ON Заказики.idКниги = Книги.idКниги
        LEFT JOIN ОптовыеПокупатели ON Заказики.idПокупатели = ОптовыеПокупатели.idПокупателя
        '''
        cursor.execute(query)
        self.orders_data = cursor.fetchall()

        self.ui.tableWidget.setRowCount(len(self.orders_data))
        self.ui.tableWidget.setColumnCount(5)
        
        # Устанавливаем заголовки
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ['Дата заказа', 'Количество', 'Скидка', 'Книга', 'Покупатель']
        )
        self.ui.tableWidget.horizontalHeader().setVisible(True)
        
        for row in range(len(self.orders_data)):
            data = self.orders_data[row]
            # Колонка 1 - Дата заказа
            item_date = QTableWidgetItem()
            item_date.setText(str(data[1]))
            self.ui.tableWidget.setItem(row, 0, item_date)
            
            # Колонка 2 - Количество
            item_count = QTableWidgetItem()
            item_count.setText(str(data[2]))
            self.ui.tableWidget.setItem(row, 1, item_count)
            
            # Колонка 3 - Скидка
            item_discount = QTableWidgetItem()
            item_discount.setText(str(data[3]) + '%')
            self.ui.tableWidget.setItem(row, 2, item_discount)
            
            # Колонка 4 - Название книги
            item_book = QTableWidgetItem()
            item_book.setText(str(data[6]) if data[6] else '')
            self.ui.tableWidget.setItem(row, 3, item_book)
            
            # Колонка 5 - Фирма покупателя
            item_buyer = QTableWidgetItem()
            item_buyer.setText(str(data[7]) if data[7] else '')
            self.ui.tableWidget.setItem(row, 4, item_buyer)
        
        self.ui.tableWidget.resizeRowsToContents()
    
    def open_add(self):
        #Открыть окно добавления заказа
        self.edit_form = orders_edit_window(self)
        self.edit_form.ui.buttonBox.accepted.connect(self.edit_form.create)
        self.edit_form.exec_()
    
    def open_update(self):
        #Открыть окно редактирования заказа
        current_row = self.ui.tableWidget.currentRow()
        if current_row >= 0 and current_row < len(self.orders_data):
            self.edit_form = orders_edit_window(self)
            order_data = self.orders_data[current_row]
            
            # Заполняем поля данными
            self.edit_form.ui.lineEdit.setText(str(order_data[1]))  # Дата
            self.edit_form.ui.lineEdit_2.setText(str(order_data[2]))  # Количество
            self.edit_form.ui.lineEdit_3.setText(str(order_data[3]))  # Скидка
            self.edit_form.order_id = order_data[0]  # Сохраняем ID
            # Устанавливаем значения в комбобоксах
            # Ищем индекс элемента с нужным ID
            book_index = self.edit_form.ui.comboBox.findData(order_data[4])  # idКниги
            if book_index >= 0:
                self.edit_form.ui.comboBox.setCurrentIndex(book_index)
            
            buyer_index = self.edit_form.ui.comboBox_2.findData(order_data[5])  # idПокупатели
            if buyer_index >= 0:
                self.edit_form.ui.comboBox_2.setCurrentIndex(buyer_index)
            self.edit_form.ui.buttonBox.accepted.connect(self.edit_form.update)
            self.edit_form.exec_()
    
    def dell(self):
        #Удаление заказа
        r = self.ui.tableWidget.currentRow()
        if r == -1:
            QMessageBox.critical(self, 'Ошибка', 'Выберите заказ для удаления.', QMessageBox.Ok)
            return
        
        order_id = self.orders_data[r][0]
        
        q = QMessageBox.question(self, 'Подтвердите действие', 'Удалить заказ?', 
                                QMessageBox.Ok | QMessageBox.Cancel)
        
        if q == QMessageBox.Ok:
            try:
                cursor.execute('DELETE FROM Заказики WHERE idЗаказа=?', [order_id])
                conn.commit()
                self.read_orders()
                QMessageBox.information(self, 'Информация', 'Заказ удален.', QMessageBox.Ok)
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Ошибка удаления: {str(e)}', QMessageBox.Ok)


class orders_edit_window(QDialog):  # Окно добавления/редактирования заказа
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = orders_edit_interface()
        self.ui.setupUi(self)
        self.order_id = None
        self.load_combo_boxes()
        # Словари для хранения соответствия между названиями и ID
        self.books_dict = {}  # {название: id}
        self.buyers_dict = {}  # {фирма: id}
    def load_combo_boxes(self):#Загружаем списки книг и покупателей в комбобоксы
        # Загружаем книги
        self.ui.comboBox.clear()
        cursor.execute('SELECT idКниги, Название FROM Книги ORDER BY Название')
        books = cursor.fetchall()
        
        self.books_dict = {}
        for book_id, book_name in books:
            self.ui.comboBox.addItem(book_name, book_id)  # Храним ID как данные элемента
            self.books_dict[book_name] = book_id
        
        # Загружаем покупателей
        self.ui.comboBox_2.clear()
        cursor.execute('SELECT idПокупателя, ФирмаПокупатель FROM ОптовыеПокупатели ORDER BY ФирмаПокупатель')
        buyers = cursor.fetchall()
        
        self.buyers_dict = {}
        for buyer_id, buyer_name in buyers:
            self.ui.comboBox_2.addItem(buyer_name, buyer_id)  # Храним ID как данные элемента
            self.buyers_dict[buyer_name] = buyer_id
    
    def create(self):
        #Добавление нового заказа#
        date = self.ui.lineEdit.text()
        quantity = self.ui.lineEdit_2.text()
        discount = self.ui.lineEdit_3.text()
        book_id = self.ui.comboBox.currentData()  # Получаем сохраненный ID
        buyer_id = self.ui.comboBox_2.currentData()
        
        
        # Проверяем, что все поля заполнены
        if not date or not quantity or not discount:
            QMessageBox.critical(self, 'Ошибка', 'Заполните все поля', QMessageBox.Ok)
            return
        
        if book_id is None or buyer_id is None:
            QMessageBox.critical(self, 'Ошибка', 'Выберите книгу и покупателя', QMessageBox.Ok)
            return
        
        q = QMessageBox.question(self, 'Подтверждение', 'Добавить заказ?', 
                                QMessageBox.Ok | QMessageBox.Cancel)
        
        if q == QMessageBox.Ok:
            try:
                cursor.execute(
                    "INSERT INTO Заказики (\"Дата заказа\", Количество, Скидка, idКниги, idПокупатели) VALUES (?,?,?,?,?)",
                    [date, quantity, discount, book_id, buyer_id]
                )
                conn.commit()
                self.parent().read_orders()  # Обновляем таблицу в родительском окне
                QMessageBox.information(self, 'Информация', 'Заказ добавлен', QMessageBox.Ok)
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Ошибка добавления: {str(e)}', QMessageBox.Ok)
    def update(self):
        #Редактирование заказа
        date = self.ui.lineEdit.text()
        quantity = self.ui.lineEdit_2.text()
        discount = self.ui.lineEdit_3.text()
        
        # Получаем ID из комбобоксов
        book_id = self.ui.comboBox.currentData()
        buyer_id = self.ui.comboBox_2.currentData()
        
        if not date or not quantity or not discount:
            QMessageBox.critical(self, 'Ошибка', 'Заполните все поля', QMessageBox.Ok)
            return
        
        if book_id is None or buyer_id is None:
            QMessageBox.critical(self, 'Ошибка', 'Выберите книгу и покупателя', QMessageBox.Ok)
            return
        
        q = QMessageBox.question(self, 'Подтверждение', 'Изменить заказ?', 
                                QMessageBox.Ok | QMessageBox.Cancel)
        
        if q == QMessageBox.Ok:
            try:
                cursor.execute(
                    "UPDATE Заказики SET \"Дата заказа\"=?, Количество=?, Скидка=?, idКниги=?, idПокупатели=? WHERE idЗаказа=?",
                    [date, quantity, discount, book_id, buyer_id, self.order_id]
                )
                conn.commit()
                self.parent().read_orders()
                QMessageBox.information(self, 'Информация', 'Заказ обновлен', QMessageBox.Ok)
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Ошибка изменения: {str(e)}', QMessageBox.Ok)
class buyers_window(QWidget):  # Окно со списком оптовых покупателей
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = buyers_interface()
        self.ui.setupUi(self)
        self.read_buyers()
        self.ui.pushButton.clicked.connect(self.open_add)  # Добавить
        self.ui.pushButton_2.clicked.connect(self.dell)    # Удалить
        self.ui.tableWidget.itemDoubleClicked.connect(self.open_update)  # Редактировать по двойному клику
    
    def read_buyers(self):
        #Чтение данных из таблицы ОптовыеПокупатели
        self.ui.tableWidget.setRowCount(0)
        cursor.execute('SELECT * FROM ОптовыеПокупатели')
        self.buyers_data = cursor.fetchall()

        self.ui.tableWidget.setRowCount(len(self.buyers_data))
        self.ui.tableWidget.setColumnCount(2)
        
        # Устанавливаем заголовки
        self.ui.tableWidget.setHorizontalHeaderLabels(['Фирма покупатель', 'Город'])
        self.ui.tableWidget.horizontalHeader().setVisible(True)
        
        for row in range(len(self.buyers_data)):
            # Колонка 0 - Фирма
            item_firm = QTableWidgetItem()
            item_firm.setText(str(self.buyers_data[row][1]))  # ФирмаПокупатель
            self.ui.tableWidget.setItem(row, 0, item_firm)
            
            # Колонка 1 - Город
            item_city = QTableWidgetItem()
            item_city.setText(str(self.buyers_data[row][2]))  # Город
            self.ui.tableWidget.setItem(row, 1, item_city)
        
        self.ui.tableWidget.resizeRowsToContents()
    
    def open_add(self):
        #Открыть окно добавления покупателя
        self.edit_form = buyers_edit_window(self)
        self.edit_form.ui.buttonBox.accepted.connect(self.edit_form.create)
        self.edit_form.exec_()
    
    def open_update(self):
        #Открыть окно редактирования покупателя
        current_row = self.ui.tableWidget.currentRow()
        if current_row >= 0 and current_row < len(self.buyers_data):
            self.edit_form = buyers_edit_window(self)
            buyer_data = self.buyers_data[current_row]
            
            # Заполняем поля данными
            self.edit_form.ui.lineEdit.setText(str(buyer_data[1]))  # Фирма
            self.edit_form.ui.lineEdit_2.setText(str(buyer_data[2]))  # Город
            self.edit_form.buyer_id = buyer_data[0]  # Сохраняем ID
            
            self.edit_form.ui.buttonBox.accepted.connect(self.edit_form.update)
            self.edit_form.exec_()
    
    def dell(self):
        #Удаление покупателя
        r = self.ui.tableWidget.currentRow()
        if r == -1:
            QMessageBox.critical(self, 'Ошибка', 'Выберите покупателя для удаления.', QMessageBox.Ok)
            return
        
        buyer_id = self.buyers_data[r][0]
        
        # Проверяем, есть ли заказы у этого покупателя
        cursor.execute('SELECT COUNT(*) FROM Заказики WHERE idПокупатели=?', [buyer_id])
        count = int(cursor.fetchone()[0])
        
        if count == 0:
            q = QMessageBox.question(self, 'Подтвердите действие', 'Удалить покупателя?', 
                                    QMessageBox.Ok | QMessageBox.Cancel)
            if q == QMessageBox.Ok:
                try:
                    cursor.execute('DELETE FROM ОптовыеПокупатели WHERE idПокупателя=?', [buyer_id])
                    conn.commit()
                    self.read_buyers()
                    QMessageBox.information(self, 'Информация', 'Покупатель удален.', QMessageBox.Ok)
                except Exception as e:
                    QMessageBox.critical(self, 'Ошибка', f'Ошибка удаления: {str(e)}', QMessageBox.Ok)
        else:
            QMessageBox.critical(self, 'Ошибка', 'Нельзя удалить покупателя, у которого есть заказы.', QMessageBox.Ok)


class buyers_edit_window(QDialog):  # Окно добавления/редактирования покупателя
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = buyers_edit_interface()
        self.ui.setupUi(self)
        self.buyer_id = None  # ID для редактирования
    
    def create(self):
        #Добавление нового покупателя
        data = [
            self.ui.lineEdit.text(),   # Фирма
            self.ui.lineEdit_2.text()   # Город
        ]
        
        if any([item == '' for item in data]):
            QMessageBox.critical(self, 'Ошибка', 'Заполните все поля', QMessageBox.Ok)
            return
        
        q = QMessageBox.question(self, 'Подтверждение', 'Добавить покупателя?', 
                                QMessageBox.Ok | QMessageBox.Cancel)
        
        if q == QMessageBox.Ok:
            try:
                cursor.execute("INSERT INTO ОптовыеПокупатели (ФирмаПокупатель, Город) VALUES (?,?)", data)
                conn.commit()
                self.parent().read_buyers()  # Обновляем таблицу в родительском окне
                QMessageBox.information(self, 'Информация', 'Покупатель добавлен', QMessageBox.Ok)
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Ошибка: {str(e)}', QMessageBox.Ok)
    
    def update(self):
        #Редактирование покупателя
        data = [
            self.ui.lineEdit.text(),   # Фирма
            self.ui.lineEdit_2.text(),  # Город
            self.buyer_id               # ID для WHERE
        ]
        
        if any([item == '' for item in data[:-1]]):
            QMessageBox.critical(self, 'Ошибка', 'Заполните все поля', QMessageBox.Ok)
            return
        
        q = QMessageBox.question(self, 'Подтверждение', 'Изменить данные покупателя?', 
                                QMessageBox.Ok | QMessageBox.Cancel)
        
        if q == QMessageBox.Ok:
            try:
                cursor.execute("UPDATE ОптовыеПокупатели SET ФирмаПокупатель=?, Город=? WHERE idПокупателя=?", data)
                conn.commit()
                self.parent().read_buyers()
                QMessageBox.information(self, 'Информация', 'Данные обновлены', QMessageBox.Ok)
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Ошибка: {str(e)}', QMessageBox.Ok)
class menuWindow(QWidget):  # Окно выбора таблицы
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = menu_interface()
        self.ui.setupUi(self)
        
        # Подключаем кнопки
        self.ui.pushButton_2.clicked.connect(self.open_knigi)  # Книги
        self.ui.pushButton_3.clicked.connect(self.open_buyers)  # Оптовые покупатели
        self.ui.pushButton_4.clicked.connect(self.open_orders)  # Заказы
        self.ui.pushButton.clicked.connect(self.ex) #Выход
    # Окна таблиц (будут созданы при первом открытии)
        self.knigi_window = None
        self.buyers_window = None
        self.orders_window = None
    def ex(self):
        menu_form.close()
    def open_knigi(self):
        global main_form
        #Открыть таблицу книг
        if self.knigi_window is None:
            self.knigi_window = main_window()
        main_form = self.knigi_window
        self.knigi_window.show()  # Показываем его
      
    
    def open_buyers(self):
        global main_form
        #Открыть таблицу заказы
        if self.buyers_window is None:
            self.buyers_window = buyers_window()
        self.buyers_window.show()  # Показываем его
    
    def open_orders(self):
        #Открыть таблицу заказов
        if self.orders_window is None:
            self.orders_window = orders_window()
        self.orders_window.show()
       
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

        self.ui.pushButtonPhoto.clicked.connect(self.select_photo)#Выбор фото
    def select_photo(self): #Фото
        try:
            filename = QFileDialog.getOpenFileName(
                self, 'Выберите фото', '', 'Images (*.jpg *.png *.jpeg *.bmp)'
            )[0]
            if filename:
                # Проверка размера (опционально)
                im = Image.open(filename)
                w, h = im.size
                if w <= 700 and h <= 700:  # можно настроить размер
                    self.ui.lineEdit_8.setText(filename)
                else:
                    QMessageBox.critical(self, 'Ошибка', 'Размер изображения превышает 700x700 пикселей.', QMessageBox.Ok)
        except Exception as e:
            print(e)
    def create_partner(self):
        photo_path = self.ui.lineEdit_8.text()#поле для фото
        partner_data = [
            self.ui.lineEdit.text(),  # Название
            self.ui.lineEdit_2.text(),  # Издательство
            self.ui.lineEdit_3.text(),  # Автор
            self.ui.lineEdit_4.text(),  # Год издания
            self.ui.lineEdit_5.text(),  # Цена
            ' '  # Фото
        ]
        if any([item == ' ' for item in partner_data[:-1]]): #Проверка на пустые значения
            QMessageBox.critical(self, 'Действие не выполнено',  'Заполните поля', QMessageBox.Ok)
            return
        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите добавить?', QMessageBox.Ok | QMessageBox.Cancel)
        if q == QMessageBox.Ok:
            try:
                cursor.execute("INSERT INTO Книги (Название, Издательство, Автор, \"Год издания\", Цена, Фото) VALUES (?,?,?,?,?,?)", partner_data)
                conn.commit()
                new_id = cursor.lastrowid #Получ. фото для новой книги
                #Если есть фото, обрабатываем его
                if photo_path:
                    # Создаем папку imports, если её нет
                    if not os.path.exists('imports'):
                        os.makedirs('imports')
                    
                    # Получаем расширение файла
                    file_ext = photo_path.split('.')[-1]
                    
                    # Создаем уникальное имя файла на основе ID книги
                    photo_name = f"book_{new_id}.{file_ext}"
                    
                    # Копируем фото с новым именем
                    shutil.copy(photo_path, 'imports/' + photo_name)
                    #Обновляем запись с правильным именем фото
                    cursor.execute("UPDATE Книги SET Фото=? WHERE idКниги=?", [photo_name, new_id])
                    conn.commit()


                    
                main_form.read_partners() #Обновление списка партнеров на главное окне
                QMessageBox.information(self, 'Действие выполнено' , 'Добавлен', QMessageBox.Ok)
                self.accept() #Закрытие диалоговое окна
                return
            except Exception as e:
                QMessageBox.critical(self, 'Действие не выполнено', f'Ошибка добавления: {str(e)}', QMessageBox.Ok)
    def update_partner(self):
        photo_path = self.ui.lineEdit_8.text()#поле для фото
        # Получаем ID книги
        book_id = self.parent().books_data[self.parent().ui.tableWidget.currentRow()][0]
    
        # Получаем старое фото из БД
        cursor.execute('SELECT Фото FROM Книги WHERE idКниги=?', [book_id])
        old_photo = cursor.fetchone()[0]
        if old_photo is None:
            old_photo = ' '
        # Обработка нового фото
        if photo_path:  # если выбрали новое фото
            file_ext = photo_path.split('.')[-1]  # расширение файла
            photo_name = f"book_{book_id}.{file_ext}"
        else:
            photo_name = old_photo  # оставляем старое фото
            
        partner_data = [
            self.ui.lineEdit.text(),  # Название
            self.ui.lineEdit_2.text(),  # Издательство
            self.ui.lineEdit_3.text(),  # Автор
            self.ui.lineEdit_4.text(),  # Год издания
            self.ui.lineEdit_5.text(),  # Цена
            photo_name # Фото
        ]
        if any([item == ' ' for item in partner_data[:-1]]): #Проверка на пустые значения
            QMessageBox.critical(self, 'Действие не выполнено',  'Заполните поля', QMessageBox.Ok)
            return
        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите изменить?', QMessageBox.Ok | QMessageBox.Cancel)
        if q == QMessageBox.Ok:
            try:
                # Копируем новое фото
                if photo_path:
                    if not os.path.exists('imports'):
                        os.makedirs('imports')
                    # Копируем новое фото
                    shutil.copy(photo_path, 'imports/' + photo_name)
                cursor.execute("UPDATE Книги SET Название=?, Издательство=?, Автор=?, \"Год издания\"=?, Цена=?, Фото=? WHERE idКниги=?", partner_data + [book_id])
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
        cursor.execute('SELECT idКниги, Скидка FROM Заказики')
        self.orders_data  = {i[0]: i[1] for i in cursor.fetchall()}

        self.ui.tableWidget.setRowCount(len(self.books_data))
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setIconSize(QSize(100, 100))  # Размер иконок
        # Устанавливаем заголовки
        self.ui.tableWidget.setHorizontalHeaderLabels(['Фото', 'Информация о книге', 'Скидка'])
        self.ui.tableWidget.horizontalHeader().setVisible(True)
        for row in range(len(self.books_data)):
            # Колонка с фото
            item_photo = QTableWidgetItem()
            photo_name = self.books_data[row][6] if len(self.books_data[row]) > 6 else ' '  # Фото
            if photo_name and photo_name.strip() and os.path.exists('imports/' + photo_name):
                item_photo.setIcon(QIcon('imports/' + photo_name))
            else:
                # Заглушка, если нет фото
                if os.path.exists('imports/no_image.png'):
                    item_photo.setIcon(QIcon('imports/no_image.png'))
            self.ui.tableWidget.setItem(row, 0, item_photo)
            # Формируем текст для второй колонки
            text = (self.books_data[row][1] + ' | ' + self.books_data[row][2]# Название | Издательство
                    + '\n' + self.books_data[row][3] # Автор
                    + '\n + Год: ' + self.books_data[row][4] + '\nЦена: ' # Год издания
                    + str(self.books_data[row][5])+ ' руб.')
            item = QTableWidgetItem()
            item.setText(text)
            self.ui.tableWidget.setItem(row,1,item)
            item = QTableWidgetItem()
            # Получаем общее количество заказов для текущей книги
            
            discount = self.orders_data.get(self.books_data[row][0], 0)  # Получаем скидку
            item.setText(str(discount) + '%')  # Выводим как есть
            self.ui.tableWidget.setItem(row, 2, item)
    
            self.ui.tableWidget.resizeRowsToContents()
app = QApplication(sys.argv)#создание объекта главного окна
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

try:
    cursor.execute("ALTER TABLE Книги ADD COLUMN Фото TEXT")
    conn.commit()
except:
    pass

# Создаем папку для фото, если её нет
if not os.path.exists('imports'):
    os.makedirs('imports')

main_form = None #Окно меню создаем
login_form = loginWindow() #Окно логина создаем и показываем
result = login_form.exec_()#Запускаем окно логина
if result == QDialog.Accepted: #Если пользователь нажал ОК
    menu_form = menuWindow() #Создаем и показываем экран с кнопками
    menu_form.show()
    sys.exit(app.exec_())
else: #Если cancel, то выход
    cursor.close()
    conn.close()
    sys.exit()

