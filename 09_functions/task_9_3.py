# -*- coding: utf-8 -*-
'''
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора
и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов, а значения access VLAN:
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN:
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

# Входные данные


def get_int_vlan_map(config_filename):
    with open(config_filename, 'r') as config:
        access = {}
        trunk = {}
        for line in config:
            list_line = line.split()
            if 'interface' in line:
                interface = list_line[1]
            elif 'access vlan' in line:
                access[interface] = int(list_line[3])
            elif 'allowed vlan' in line:
                trunk[interface] = [int(i) for i in list_line[4].split(',')]   
    return access, trunk

# Выполнение программы

print(get_int_vlan_map('config_sw1.txt'))

# Пауза
input()