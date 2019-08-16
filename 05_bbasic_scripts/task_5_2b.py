# -*- coding: utf-8 -*-
'''
Задание 5.2b

Преобразовать скрипт из задания 5.2a таким образом,
чтобы сеть/маска не запрашивались у пользователя,
а передавались как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

#!/usr/bin/env python

import sys
print(sys.argv)

prefix = sys.argv[1]
ip, mask = prefix.split('/')
ip_oct1, ip_oct2, ip_oct3, ip_oct4 = int(ip.split('.')[0]), int(ip.split('.')[1]), int(ip.split('.')[2]), int(ip.split('.')[3])
mask_str = '1' * int(mask) + '0' * (32 - int(mask))
mask_oct1, mask_oct2, mask_oct3, mask_oct4 = int(mask_str[0:8],2), int(mask_str[8:16],2), int(mask_str[16:24],2), int(mask_str[24:32],2)
host_oct1, host_oct2, host_oct3, host_oct4 = ip_oct1 & mask_oct1, ip_oct2 & mask_oct2, ip_oct3 & mask_oct3, ip_oct4 & mask_oct4
print(f'''
Network:
{host_oct1:<8}  {host_oct2:<8}  {host_oct3:<8}  {host_oct4:<8}
{host_oct1:08b}  {host_oct2:08b}  {host_oct3:08b}  {host_oct4:08b}

Mask:
/{mask}
{mask_oct1:<8}  {mask_oct2:<8}  {mask_oct3:<8}  {mask_oct4:<8}
{mask_oct1:08b}  {mask_oct2:08b}  {mask_oct3:08b}  {mask_oct4:08b}''')

input()
