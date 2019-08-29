# -*- coding: utf-8 -*-
'''
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Дополнить скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

vlan = input('Введите номер VLAN (10,100,200,300,500,1000): ')
new = []
with open('CAM_table.txt') as file:
    for stroka in file:
        stroka = stroka.split()
        if stroka and stroka[0].isdigit() and stroka[0] == vlan:
            new.append([int(stroka[0]), stroka[1], stroka[3]])
for o,t,f in new:
    print(f"{o:<7}{t:17}{f:5}")
input()  