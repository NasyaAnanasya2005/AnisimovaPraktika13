import sqlite3
#Создаем подключение к базе данных (файл database.db будет создан)
connection  = sqlite3.connect ( 'database .db' )
cursor =connection.cursor()
"""#Получаю средний возраст пользователей для каждого возраста
cursor.execute('SELECT age, AVG (age) FROM Users GROUP BY age')
users = cursor.fetchall()
for user in users:
    print(user)


#Фильтруем группы по среднему возрасту больше 20
cursor.execute('SELECT age, AVG (age) FROM Users GROUP BY age HAVING AVG(age) > ?',(30,))
us = cursor.fetchall()
for userq in us:
    print(userq)

#Выбираю и сортирую пользователей по возрасту по убыванию
cursor.execute('SELECT username, age FROM Users ORDER BY age DESC')
users = cursor.fetchall()
for user in users:
    print(user)"""
#Комбинировала операторы для выполнения более сложных запросов
cursor.execute('''SELECT username, age, AVG(age) FROM Users GROUP BY age HAVING AVG(age) > ? ORDER BY age DESC ''', (20,))
users = cursor.fetchall()
for user in users:
    print(user)

connection.close()
