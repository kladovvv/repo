# -*- coding: utf-8 -*-
'''
Задание 22.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM

Функция должна подключаться к одному устройству, отправлять команду show с помощью netmiko,
а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 22.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br и устройствах из devices.yaml.
'''
import textfsm
import yaml
import netmiko
import os


def send_and_parse_show_command(device_dict, command, templates_path):
    with netmiko.ConnectHandler(**device_dict) as ssh:
        output = ssh.send_command(command)
    path = os.path.join(templates_path, 'sh_ip_int_br.template')
    with open(path) as template:
        fsm = textfsm.TextFSM(template)
        data = fsm.ParseTextToDicts(output)
    return data


with open('devices.yaml') as dev:
    devices = yaml.safe_load(dev)
command = 'sh ip int br'
templates = os.path.join(os.getcwd(), 'templates')
for device in devices:
    print(device['ip'])
    print(send_and_parse_show_command(device, command, templates))
