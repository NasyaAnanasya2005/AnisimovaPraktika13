import sqlite3
#Создаем подключение к базе данных (файл database.db будет создан)
connection  = sqlite3.connect ( 'database .db' )
cursor =connection.cursor()

cursor.execute('UPDATE Users SET age = ? WHERE username = ?', (29, 'Oleg'))
connection.commit()
connection.close()
