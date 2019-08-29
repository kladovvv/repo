# -*- coding: utf-8 -*-
'''
Задание 7.2c

Переделать скрипт из задания 7.2b:
* передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

Внутри, скрипт должен отфильтровать те строки, в исходном файле конфигурации,
в которых содержатся слова из списка ignore.
И записать остальные строки в итоговый файл.

Проверить работу скрипта на примере файла config_sw1.txt.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

import sys

ignore = ['duplex', 'alias', 'Current configuration']

with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as dest:
    for line in f:
        line_list = line.split()
        for i in ignore:
            if i in line_list:
                break
        else:
            dest.write(line.rstrip() + '\n')        
