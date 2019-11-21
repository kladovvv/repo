import sqlite3
import os
import yaml
import re

def add_data_switches(db):
    conn = sqlite3.connect(db)
    with open('switches.yml') as f:
        switch_dict = yaml.safe_load(f)
    result = [(key, value) for v in switch_dict.values() for key, value in v.items()]
    print('Добавляю данные в таблицу switches...')
    for row in result:
        try:
            with conn:
                query = 'INSERT into switches values (?, ?)'
                conn.execute(query, row)
        except sqlite3.IntegrityError as error:
            print(f'''При добавлении данных: {row} Возникла ошибка: ''', error)
    conn.close()


def add_data_dhcp(db, list_of_files):
    conn = sqlite3.connect(db)
    print('Добавляю данные в таблицу dhcp...')
    for file in list_of_files:
        switch = re.match('(\S+)_dhcp', file).group(1)
        with open(file) as snoop:
            result = re.findall('(?P<mac>\S+) +(?P<ip>\S+) +\d+ +\S+ +(?P<vlan>\d+) +(?P<int>\S+)' , snoop.read())
        for row in result:
            try:
                with conn:
                    row += (switch,)
                    query = 'INSERT into dhcp values (?, ?, ?, ?, ?)'
                    conn.execute(query, row)
            except sqlite3.IntegrityError as error:
                print(f'''При добавлении данных: {row} Возникла ошибка: ''', error)
    conn.close()


db_ex = 'dhcp_snooping.db'
db_exist = os.path.exists('dhcp_snooping.db')
list_of_f = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
if db_exist:
    add_data_switches(db_ex)
    add_data_dhcp(db_ex, list_of_f)
else:
    print('База данных не существует. Перед добавлением данных, ее надо создать')