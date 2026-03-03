import sqlite3
#Создаем подключение к базе данных (файл database.db будет создан)
connection  = sqlite3.connect ( 'database .db' )
cursor =connection.cursor()
data = [('Nasya', 'Nasya05@mail.ru',20), ('Oleg', 'Oleg05@mail.ru',23), ('Bali', 'Bali05@mail.ru',24), ('Vasya', 'Vasya05@mail.ru',24)]
cursor.execute('INSERT INTO Users (username, email, age) VALUES (?,?,?)', ('Vasya', 'Vasya05@mail.ru',24))
connection.commit()
connection.close()
