import sqlite3
#Создаем подключение к базе данных (файл database.db будет создан)
connection  = sqlite3.connect ( 'database .db' )
cursor =connection.cursor()
# Создаем таблицу Users
cursor.execute('CREATE INDEX idx_email ON Users (email) ')
# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()
