import sqlite3
import os
from time import sleep


class InitTableError(Exception):
    ...


def initiate_db(db_name='Products'):
    # Проверка на существование базы данных с таким названием
    if f'{db_name}.db' in os.listdir(os.getcwd()):
        raise InitTableError(f'База данных с именем {db_name} УЖЕ существует!')

    # Создание базы данных с названием, переданным в аргументе функции
    conn = sqlite3.connect(f'{db_name}.db')
    cur = conn.cursor()

    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {db_name}(
        id INTEGER IF PRIMARY KEY,
        title TEXT IF NOT NULL,
        description TEXT,
        price INTEGER IF NOT NULL
        ) 
    """)

    conn.commit()
    conn.close()


def put_in_db(id_: int, title: str, price: int, description: str = None, img: str = None, db_name='Products'):
    if not f'{db_name}.db' in os.listdir(os.getcwd()):
        raise InitTableError(f'База данных с именем {db_name} НЕ существует!')

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


def get_all_products(db_name='Products'):
    if not f'{db_name}.db' in os.listdir(os.getcwd()):
        raise InitTableError(f'Базы данных с именем {db_name} НЕ существует!')

    # Open
    conn = sqlite3.connect(f'{db_name}.db')
    cur = conn.cursor()

    cur.execute(f'SELECT * FROM {db_name}')
    data_from_db = cur.fetchall()

    # Close
    conn.commit()
    conn.close()
    return data_from_db
