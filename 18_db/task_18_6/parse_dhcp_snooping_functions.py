import sqlite3
import os
from tabulate import tabulate
import yaml
import re
from datetime import timedelta, datetime


def create_db(db_filename, schema):
    p = os.path.exists(db_filename)
    if not p:
        conn = sqlite3.connect(db_filename)
        with open(schema) as file:
            print('Создаю базу данных...')
            conn.executescript(file.read())
    else:
        print('База данных существует')


def add_data_switches(db, filename):
    conn = sqlite3.connect(db)
    with open(filename[0]) as f:
        switch_dict = yaml.safe_load(f)
    result = [(key, value) for v in switch_dict.values() for key, value in v.items()]
    print('Добавляю данные в таблицу switches...')
    for row in result:
        with conn:
            query = 'REPLACE into switches values (?, ?)'
            conn.execute(query, row)
    conn.close()


def add_data(db, list_of_files):
    now = datetime.today().replace(microsecond=0)
    week_ago = now - timedelta(days=7)
    conn = sqlite3.connect(db)
    print('Добавляю данные в таблицу dhcp...')
    conn.execute('UPDATE dhcp set active = 0')
    for file in list_of_files:
        switch = re.search(r'(sw\d)_dhcp', file).group(1)
        with open(file) as snoop:
            result = re.findall('(?P<mac>\S+) +(?P<ip>\S+) +\d+ +\S+ +(?P<vlan>\d+) +(?P<int>\S+)' , snoop.read())
        for row in result:
            with conn:
                row += (switch, 1)
                query = '''REPLACE into dhcp values (?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))'''
                conn.execute(query, row)
    check = conn.execute('select last_active from dhcp where active = 0')
    while True:
        next_row = check.fetchone()
        if next_row:
            if str(week_ago) > next_row[0]:
                with conn:
                    q = 'delete from dhcp where last_active = ?'
                    conn.execute(q, next_row)
        else:
            break
    headers = ['mac', 'ip', 'vlan', 'interface', 'switch', 'active', 'last_active']
    print(tabulate(conn.execute('SELECT * from dhcp'), headers=headers))
    conn.close()


def get_all_data(db_filename):
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    headers = ['mac', 'ip', 'vlan', 'interface', 'switch', 'active', 'last_active']
    c.execute('SELECT * from dhcp where active = 1')
    print('Активные записи:')
    print(tabulate(c.fetchall(), headers=headers))
    c.execute('SELECT * from dhcp where active = 0')
    next_row = c.fetchone()
    if next_row:
        print('Неактивные записи:')
        print(tabulate(c.execute('SELECT * from dhcp where active = 0'), headers=headers))
    conn.close()


def get_data(db_filename, *args):
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    key, value = args
    keys = ['mac', 'ip', 'vlan', 'interface', 'switch']
    if key in keys:
        keys.remove(key)
    else:
        return print('Данный параметр не поддерживается.\n'
                     'Допустимые значения параметров: mac, ip, vlan, interface, switch')
    query_1 = 'SELECT * from dhcp where {} = ? and active = 1'.format(key)
    query_2 = 'SELECT * from dhcp where {} = ? and active = 0'.format(key)
    headers = ['mac', 'ip', 'vlan', 'interface', 'switch', 'active', 'last_active']
    c.execute(query_1, (value,))
    print('Активные записи:')
    print(tabulate(c.fetchall(), headers=headers))
    c.execute(query_2, (value,))
    next_row = c.fetchone()
    if next_row:
        print('Неактивные записи:')
        print(tabulate(c.execute(query_2, (value,)), headers=headers))
    conn.close()
