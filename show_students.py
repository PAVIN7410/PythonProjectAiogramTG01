import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('school_data.db')
cursor = conn.cursor()

# Выполнение запроса
cursor.execute('SELECT * FROM students')
rows = cursor.fetchall()

# Вывод всех записей
for row in rows:
    print(row)

# Закрытие соединения
conn.close()