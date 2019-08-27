# -*- coding: utf-8 -*-
'''
Задание 6.2a
Сделать копию скрипта задания 6.2.
Добавить проверку введенного IP-адреса. Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой,
   - каждое число в диапазоне от 0 до 255.
Если адрес задан неправильно, выводить сообщение:
'Неправильный IP-адрес'
Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

ip_correct = False
while not ip_correct:
    ip = input('Введите IP-адрес: ')
    ip_list = ip.split('.')
    if len(ip_list) != 4:
        print('Неправильный IP-адрес')
        continue
    for i in ip_list:
        try:
            if int(i) not in range(0, 256):    
                print('Неправильный IP-адрес')
                break
        except ValueError:
            print('Неправильный IP-адрес')
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
