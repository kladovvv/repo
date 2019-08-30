# -*- coding: utf-8 -*-
'''
Задание 4.7

Преобразовать MAC-адрес mac в двоичную строку такого вида:
'101010101010101010111011101110111100110011001100'

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

mac = 'AAAA:BBBB:CCCC'
template = '{:b}{:b}{:b}'
mac_split = mac.split(':')
mac_1 = int(mac_split[0], 16)
mac_2 = int(mac_split[1], 16)
mac_3 = int(mac_split[2], 16)
print(template.format(mac_1, mac_2, mac_3))
print(f"{mac_1:b}{mac_2:b}{mac_3:b}")

input()
