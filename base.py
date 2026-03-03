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
    print(user)
#Комбинировала операторы для выполнения более сложных запросов
cursor.execute('''SELECT username, age, AVG(age) FROM Users GROUP BY age HAVING AVG(age) > ? ORDER BY age DESC ''', (20,))
users = cursor.fetchall()
for user in users:
    print(user)
#Подсчет общего числа пользователей
cursor.execute('SELECT COUNT(*) FROM Users')
users = cursor.fetchone()[0]
print("Общее кол-во пользователей: ", users)
connection.close()

#Вычисление суммы возрастов пользователей SUM
cursor.execute('SELECT SUM(age) FROM Users')
users = cursor.fetchone()[0]
print("Общая сумма возрастов пользователей: ", users)


#AVG
cursor.execute('SELECT AVG(age) FROM Users')
userss = cursor.fetchone()[0]
print("Средний возраст пользователей: ", userss)


#MIN
cursor.execute('SELECT MIN(age) FROM Users')
usersss = cursor.fetchone()[0]
print("Минимальный возраст пользователей: ", usersss)


#MAX
cursor.execute('SELECT MAX(age) FROM Users')
userssss = cursor.fetchone()[0]
print("Максимальный возраст пользователей: ", userssss)"""

#Сложные запросы
cursor.execute('''SELECT username, age FROM Users WHERE age = (SELECT MAX(age) FROM Users)''')
users = cursor.fetchall()
for user in users:
    print(user)
connection.close()
