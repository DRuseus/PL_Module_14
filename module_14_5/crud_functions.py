import sqlite3
import os
from time import sleep


class DataBaseError(Exception):
    ...


def initiate_db(db_name='telegram_database'):

    # Создание базы данных с названием, переданным в аргументе функции
    conn = sqlite3.connect(f'{db_name}.db')
    cur = conn.cursor()

    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER IF PRIMARY KEY,
        title TEXT IF NOT NULL,
        description TEXT,
        price INTEGER IF NOT NULL
        ) 
    """)

    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT IF NOT NULL,
        email TEXT IF NOT NULL,
        age INTEGER IF NOT NULL,
        balance INTEGER IF NOT NULL
        ) 
    """)

    conn.commit()
    conn.close()


def add_user(username, email, age, db_name='telegram_database'):
    if not f'{db_name}.db' in os.listdir(os.getcwd()):
        raise DataBaseError(f'База данных с именем {db_name} НЕ существует!')

    # Open
    conn = sqlite3.connect(f'{db_name}.db')
    cur = conn.cursor()

    # Это нужно для определения присваиваемого индекса
    users_count = cur.execute('SELECT MAX(id) FROM Users').fetchone()

    cur.execute(f'INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)',
                    (username, email, age, 1000))
    # Close
    conn.commit()
    conn.close()


def check_user(username, db_name='telegram_database'):
    if not f'{db_name}.db' in os.listdir(os.getcwd()):
        raise DataBaseError(f'База данных с именем {db_name} НЕ существует!')

    # Open
    conn = sqlite3.connect(f'{db_name}.db')
    cur = conn.cursor()

    # Это проверка на дубликацию юзера в БД по параметру "username"
    result = cur.execute('SELECT COUNT(username) FROM Users WHERE username= ?', (username, )).fetchone()
    print(result[0])
    # Close
    conn.commit()
    conn.close()
    return result[0]


def put_in_prod(id_: int, title: str, price: int, description: str = None, db_name='telegram_database'):
    if not f'{db_name}.db' in os.listdir(os.getcwd()):
        raise DataBaseError(f'База данных с именем {db_name} НЕ существует!')

    # Open
    conn = sqlite3.connect(f'{db_name}.db')
    cur = conn.cursor()

    try:
       cur.execute(f'INSERT INTO Products VALUES(?, ?, ?, ?)',
               (id_, title, description, price))
    except:
        print('Уже есть такой товар')

    # Close
    conn.commit()
    conn.close()


def get_all_products(db_name='telegram_database'):
    if not f'{db_name}.db' in os.listdir(os.getcwd()):
        raise DataBaseError(f'Базы данных с именем {db_name} НЕ существует!')

    # Open
    conn = sqlite3.connect(f'{db_name}.db')
    cur = conn.cursor()

    cur.execute(f'SELECT * FROM Products')
    data_from_db = cur.fetchall()

    # Close
    conn.commit()
    conn.close()
    return data_from_db
