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
print("Максимальный возраст пользователей: ", userssss)

#Сложные запросы
cursor.execute('''SELECT username, age FROM Users WHERE age = (SELECT MAX(age) FROM Users)''')
users = cursor.fetchall()
for user in users:
    print(user)

#Получение результатов запроса в виде списка кортежей
cursor.execute('SELECT * FROM Users ')
users = cursor.fetchall()
for user in users:
    print(user)
#Выбираю первого пользователя
cursor.execute('SELECT * FROM Users ')
u = cursor.fetchone()
for user in u:
    print(user)

    #Выбираю первых 5-ти пользователей
cursor.execute('SELECT * FROM Users ')
us = cursor.fetchmany(5)
for user in us:
    print(user)

    #Выбираю всех пользователей
cursor.execute('SELECT * FROM Users ')
use = cursor.fetchall()
for user in use:
    print(user)
#Выбираю всех пользователей
cursor.execute('SELECT * FROM Users ')
use = cursor.fetchall()
users_list = []
#Преобразую результаты в список словарей
for user in use:
    users_dict = { 'id': user[0], 'username': user[1], 'email': user[2], 'age': user[3]}
    users_list.append(users_dict)
#выводим результат
for user in users_list:
    print(user)

#Выбираю пользователей с неизвестным возрастом(у меня таких нет)
cursor.execute('SELECT * FROM Users WHERE age IS NULL ')
unknown_age_users = cursor.fetchall()
for user in unknown_age_users:
    print(user)

#Использование операторов BEGIN, COMMIT и ROLLBACK
try:
    #Начинаем транзакцию
    cursor.execute('BEGIN')

    #Операции выполняю, заполняю
    cursor.execute('INSERT INTO Users (username,email) VALUES (?,?)', ('nina', 'nina05@mail.ru'))
    cursor.execute('INSERT INTO Users (username,email) VALUES (?,?)', ('jija', 'jija05@mail.ru'))    
    #Подтверждаю изменения
    cursor.execute('COMMIT')

except:
    #Отменяем транзацию в случае ошибки
    cursor.execute('ROLLBACK')

#Автоматическое управление транзакциями с помощью комплексных менеджеров

try:
    #Начинаем транзакцию avto
    with connection:
        #Операции выполняю, заполняю
        cursor.execute('INSERT INTO Users (username,email) VALUES (?,?)', ('vika', 'vvika05@mail.ru'))
        cursor.execute('INSERT INTO Users (username,email) VALUES (?,?)', ('lexa', 'lixach05@mail.ru'))    
    #Подтверждаю изменения
    cursor.execute('COMMIT')

except:
    #Ошибки буду приводить к автоматическому откату транзакции
    pass

#Использование подготовленных запросов для повышения производительности
query = 'SELECT * FROM Users WHERE age > ?'
cursor.execute(query, (23,))
users = cursor.fetchall()
for user in users:
    print(user)

#Создаем представление для активных пользователей
cursor.execute('CREATE VIEW ActiveUsers AS SELECT * FROM Users WHERE id = 1')
#Выбираем активных пользователей
cursor.execute('SELECT  * FROM ActiveUsers')
users = cursor.fetchall()
#Выводим результаты
for user in users: 
    print(user)
#Создание триггеров для автоматизации операций при изменении данных
cursor.execute('''CREATE TRIGGER IF NOT EXISTS update_created_at AFTER INSERT ON Users BEGIN UPDATE Users SET created_at = CURRENT_TIMESTAMP' WHERE id = NEW.id; END; ''')

#Работа с индексами для оптимизации запросов
cursor.execute('CREATE INDEX idx_username ON Users (username) ' )"""




#Закрываем соединение
connection.commit()
connection.close()




