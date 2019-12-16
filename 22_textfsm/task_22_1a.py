# -*- coding: utf-8 -*-
'''
Задание 22.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.
'''
import textfsm
from tabulate import tabulate


def parse_output_to_dict(template, command_output):
    with open(template) as t, open(command_output) as o:
        fsm = textfsm.TextFSM(t)
        result = fsm.ParseTextToDicts(o.read())
        return result


print(tabulate(parse_output_to_dict('templates/sh_ip_int_br.template', 'output/sh_ip_int_br.txt'), headers='keys'))
