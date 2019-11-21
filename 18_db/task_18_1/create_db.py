import sqlite3
import os

db_filename = 'dhcp_snooping.db'
schema = 'dhcp_snooping_schema.sql'

def create_db():
    proverka = os.path.exists(db_filename)
    if not proverka:
        conn = sqlite3.connect(db_filename)
        with open(schema) as file:
            print('Создаю базу данных...')
            conn.executescript(file.read())
    else:
        print('База данных существует')


create_db()