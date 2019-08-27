# -*- coding: utf-8 -*-
'''
Задание 6.2b
Сделать копию скрипта задания 6.2a.
Дополнить скрипт:
Если адрес был введен неправильно, запросить адрес снова.
Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

ip_correct = False
ip = input('Введите IP-адрес: ')
while not ip_correct:
    ip_list = ip.split('.')
    if len(ip_list) != 4:
        print('Неправильный IP-адрес')
        ip = input('Введите IP-адрес заново: ')
        continue
    for i in ip_list:
        try:
            if int(i) not in range(0, 256):    
                print('Неправильный IP-адрес')
                ip = input('Введите IP-адрес заново: ')
                break
        except ValueError:
            print('Неправильный IP-адрес')
            ip = input('Введите IP-адрес заново: ')
            break
    else:
        ip_correct = True

if int(ip.split('.')[0]) in range(1,224):
    print('unicast')
elif int(ip.split('.')[0]) in range(224,240):
    print('multicast')
elif ip == '255.255.255.255':
    print('local broadcast')
elif ip == '0.0.0.0':
    print('unassigned')
else:
    print('unused')

input()