import sqlite3

conn = sqlite3.connect('not_telegram.db')
cur = conn.cursor()

# Create a database
cur.execute("""
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER IF PRIMARY KEY,
    username TEXT IF NOT NULL,
    email TEXT IF NOT NULL,
    age INTEGER,
    balance INTEGER IF NOT NULL
    ) 
""")

# Заполнение таблицы сгенерированными юзерами
users_data_gen = [(d, f"User{d}", f"example{d}@gmail.com", d*10, 1000) for d in range(1, 11)]
cur.executemany('INSERT INTO Users VALUES(?, ?, ?, ?, ?)', users_data_gen)

# Обновление баланса у каждого второго юзера, начиная с первого
cur.execute('UPDATE Users SET balance = 500 WHERE id % ?', (2, ))

# Удаление каждого третьего пользователя начиная с первого
cur.executemany('DELETE FROM Users WHERE id = ?', ([(d,) for d in range(1, 11, 3)]))

# Сделана выборка всех записей при помощи fetchall(), где возраст не равен 60
cur.execute('SELECT username, email, age, balance FROM Users WHERE age != 60')
users = cur.fetchall()
for user in users:
    print('Имя: %s | Почта: %s | Возраст: %s | Баланс: %s' % user)

conn.commit()
conn.close()
