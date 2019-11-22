import sqlite3
import sys
from tabulate import tabulate


def get_data(db_filename):
    conn = sqlite3.connect(db_filename)
    conn.row_factory = sqlite3.Row
    if len(sys.argv) == 1:
        print('В таблице dhcp такие записи:')
        result = conn.execute('SELECT * from dhcp')
        print(tabulate(result))
    elif len(sys.argv) == 3:
        _, key, value = sys.argv
        keys = ['mac', 'ip', 'vlan', 'interface', 'switch']
        if key in keys:
            keys.remove(key)
        else:
            return print('Данный параметр не поддерживается.\n'
                         'Допустимые значения параметров: mac, ip, vlan, interface, switch')
        print(f'Информация об устройствах с такими параметрами: {key} {value}')
        query = 'SELECT * from dhcp where {} = ?'.format(key)
        result = conn.execute(query, (value,))
        print(tabulate(result))
    else:
        print('Пожалуйста, введите два или ноль аргументов')
    conn.close()


db_file = 'dhcp_snooping.db'
get_data(db_file)