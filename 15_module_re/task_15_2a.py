# -*- coding: utf-8 -*-
'''
Задание 15.2a

Создать функцию convert_to_dict, которая ожидает два аргумента:
* список с названиями полей
* список кортежей со значениями

Функция возвращает результат в виде списка словарей, где ключи - взяты из первого списка,
а значения подставлены из второго.

Например, если функции передать как аргументы список headers и список
[('FastEthernet0/0', 'up', 'up', '10.0.1.1'),
 'FastEthernet0/1', 'up', 'up', '10.0.2.1')]

Функция должна вернуть такой список со словарями (порядок полей может быть другой):
[{'interface': 'FastEthernet0/0', 'status': 'up', 'protocol': 'up', 'address': '10.0.1.1'},
 {'interface': 'FastEthernet0/1', 'status': 'up', 'protocol': 'up', 'address': '10.0.2.1'}]

Проверить работу функции:
* первый аргумент - список headers
* второй аргумент - результат, который возвращает функция parse_sh_ip_int_br из задания 15.2, если ей как аргумент передать sh_ip_int_br.txt.

Функцию parse_sh_ip_int_br не нужно копировать.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''
import re
from pprint import pprint
from task_15_2 import parse_sh_ip_int_br


def convert_to_dict(head, tuples):
    result = []
    for tup in tuples:
        dic = {h: t for h, t in zip(head, tup)}
        result.append(dic)
    return result


headers = ['interface', 'address', 'status', 'protocol']
sh_ip = parse_sh_ip_int_br('sh_ip_int_br.txt')
pprint(convert_to_dict(headers, sh_ip))