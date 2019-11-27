import sqlite3
import sys
from tabulate import tabulate


def get_data(db_filename):
    conn = sqlite3.connect(db_filename)
    conn.row_factory = sqlite3.Row
    if len(sys.argv) == 1:
        print('В таблице dhcp такие записи:')
        result_1 = conn.execute('SELECT * from dhcp where active = 1')
        result_2 = conn.execute('SELECT * from dhcp where active = 0')
        print('Активные записи:')
        print(tabulate(result_1))
        while True:
            next_row = result_2.fetchone()
            if next_row:
                print('Неактивные записи:')
                print(tabulate(result_2))
            else:
                break
    elif len(sys.argv) == 3:
        _, key, value = sys.argv
        keys = ['mac', 'ip', 'vlan', 'interface', 'switch']
        if key in keys:
            keys.remove(key)
        else:
            return print('Данный параметр не поддерживается.\n'
                         'Допустимые значения параметров: mac, ip, vlan, interface, switch')
        print(f'Информация об устройствах с такими параметрами: {key} {value}')
        query_1 = 'SELECT * from dhcp where {} = ? and active = 1'.format(key)
        query_2 = 'SELECT * from dhcp where {} = ? and active = 0'.format(key)
        result_1 = conn.execute(query_1, (value,))
        result_2 = conn.execute(query_2, (value,))
        print('Активные записи:')
        print(tabulate(result_1))
        while True:
            next_row = result_2.fetchone()
            if next_row:
                print('Неактивные записи:')
                print(tabulate(result_2))
            else:
                break
    else:
        print('Пожалуйста, введите два или ноль аргументов')
    conn.close()


db_file = r'C:\Users\admin7\Documents\GitHub\repo\18_db\task_18_3\dhcp_snooping.db'
get_data(db_file)