import sqlite3
#Создаем подключение к базе данных (файл database.db будет создан)
connection  = sqlite3.connect ( 'database .db' )
cursor =connection.cursor()
#Вывожу людей старше 23 лет
cursor.execute('SELECT username, age FROM Users WHERE age > ?', (23,))
users = cursor.fetchall()
for user in users:
    print(user)

connection.close()
