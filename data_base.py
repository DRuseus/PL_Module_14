import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute(
    '''
    
    '''
)

connection.commit()
connection.close()
