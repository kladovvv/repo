# -*- coding: utf-8 -*-
'''
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт:
  Скрипт не должен выводить команды, в которых содержатся слова,
  которые указаны в списке ignore.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']
with open('config_sw1.txt') as f:
    for line in f:
        line_list = line.split()
        for i in ignore:
            if i in line_list or line.startswith('!'):
                break
        else:
            print(line.rstrip())        
input()