import sqlite3 as sq



base = sq.connect('clients.db')
cur = base.cursor()


def sql_start():
    if base:
        print('Data base conected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS clients'
                 '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                 ' tg_user_id INTEGER NOT NULL UNIQUE,'
                 ' user_name TEXT,'
                 ' phone_number INTEGER UNIQUE,'
                 ' name TEXT,'
                 ' surname TEXT,'
                 ' date_of_birth DATE)')
    base.commit()


