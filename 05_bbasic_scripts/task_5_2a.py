# -*- coding: utf-8 -*-

'''
Задание 5.2a

Всё, как в задании 5.2, но, если пользователь ввел адрес хоста, а не адрес сети,
надо преобразовать адрес хоста в адрес сети и вывести адрес сети и маску, как в задании 5.2.

Пример адреса сети (все биты хостовой части равны нулю):
* 10.0.1.0/24
* 190.1.0.0/16

Пример адреса хоста:
* 10.0.1.1/24 - хост из сети 10.0.1.0/24
* 10.0.5.1/30 - хост из сети 10.0.5.0/30

Если пользователь ввел адрес 10.0.1.1/24,
вывод должен быть таким:

Network:
10        0         1         0
00001010  00000000  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

prefix = input('Введите адрес хоста и маску в формате x.x.x.x/x: ')
ip, mask = prefix.split('/')
ip_oct1, ip_oct2, ip_oct3, ip_oct4 = int(ip.split('.')[0]), int(ip.split('.')[1]), int(ip.split('.')[2]), int(ip.split('.')[3])
mask_str = '1' * int(mask) + '0' * (32 - int(mask))
mask_oct1, mask_oct2, mask_oct3, mask_oct4 = int(mask_str[0:8],2), int(mask_str[8:16],2), int(mask_str[16:24],2), int(mask_str[24:32],2)
host_oct1, host_oct2, host_oct3, host_oct4 = ip_oct1 & mask_oct1, ip_oct2 & mask_oct2, ip_oct3 & mask_oct3, ip_oct4 & mask_oct4

#print(f'''
#Network:
#{host_oct1:<8}  {host_oct2:<8}  {host_oct3:<8}  {host_oct4:<8}
#{host_oct1:08b}  {host_oct2:08b}  {host_oct3:08b}  {host_oct4:08b}

#Mask:
#/{mask}
#{mask_oct1:<8}  {mask_oct2:<8}  {mask_oct3:<8}  {mask_oct4:<8}
#{mask_oct1:08b}  {mask_oct2:08b}  {mask_oct3:08b}  {mask_oct4:08b}''')
