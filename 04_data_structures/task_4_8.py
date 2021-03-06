# -*- coding: utf-8 -*-
'''
Задание 4.8

Преобразовать IP-адрес в двоичный формат и вывести на стандартный поток вывода вывод столбцами, таким образом:
- первой строкой должны идти десятичные значения байтов
- второй строкой двоичные значения

Вывод должен быть упорядочен также, как в примере:
- столбцами
- ширина столбца 10 символов

Пример вывода для адреса 10.1.1.1:
10        1         1         1
00001010  00000001  00000001  00000001

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ip = input("Введите IP-адрес:  ")
ip_list = ip.split('.')

print(f'''
{int(ip_list[0]):<10}{int(ip_list[1]):<10}{int(ip_list[2]):<10}{int(ip_list[3]):<10}
{int(ip_list[0]):>08b}  {int(ip_list[1]):>08b}  {int(ip_list[2]):>08b}  {int(ip_list[3]):>08b}''')

input("\nНажмите любую кнопку...")
