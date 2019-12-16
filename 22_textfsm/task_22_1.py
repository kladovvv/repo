# -*- coding: utf-8 -*-
'''
Задание 22.1

Создать функцию parse_command_output. Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список:
* первый элемент - это список с названиями столбцов
* остальные элементы это списки, в котором находятся результаты обработки вывода

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.

'''
import textfsm
from tabulate import tabulate


def parse_command_output(template, command_output):
    res_list = []
    with open(template) as templ, open(command_output) as comm:
        text = textfsm.TextFSM(templ)
        result = text.ParseText(comm.read())
        res_list.append(text.header)
        res_list.extend(result)
    return res_list


if __name__ == '__main__':
    print(tabulate(parse_command_output('templates/sh_ip_int_br.template', 'output/sh_ip_int_br.txt'), headers='firstrow'))
