# -*- coding: utf-8 -*-
'''
Задание 7.1

Аналогично заданию 4.6 обработать строки из файла ospf.txt
и вывести информацию по каждой в таком виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

h = ['Protocol: ',
 'Prefix: ',
 'AD/Metric: ',
 '_',
 'Next-Hop: ',
 'Last update: ',
 'Outbound Interface: ']
 
with open('ospf.txt') as f:
    for l in f:
        l = l.split()
        print(f'''{h[0]:<24}{l[0][0]}
{h[1]:<24}{l[1]}
{h[2]:<24}{l[2].strip('[]')}
{h[4]:<24}{l[4].rstrip(',')}
{h[5]:<24}{l[5].rstrip(',')}
{h[6]:<24}{l[6]}\n''')
input()
