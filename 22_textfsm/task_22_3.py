# -*- coding: utf-8 -*-
'''
Задание 22.3

Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* attributes_dict - словарь атрибутов, в котором находятся такие пары ключ-значение:
 * 'Command': команда
 * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами. Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - templates

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 22.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
'''
from textfsm import clitable
from pprint import pprint


def parse_command_dynamic(command_output, attributes_dict, index_file, templ_path):
    result = []
    cli_t = clitable.CliTable(index_file, templ_path)
    cli_t.ParseCmd(command_output, attributes_dict)
    for c in cli_t:
        result.append(dict(zip(list(cli_t.header), list(c))))
    pprint(result)


output_file = 'output/sh_ip_int_br.txt'
with open(output_file) as file:
    output = file.read()
comm = 'sh ip int br'
vend = 'cisco_ios'
attributes = {'Command': comm, 'Vendor': vend}
index = 'index'
templ = 'templates'
parse_command_dynamic(output, attributes, index, templ)
