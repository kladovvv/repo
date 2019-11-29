# -*- coding: utf-8 -*-
'''
Задание 19.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к одному устройству и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла devices.yaml с помощью функции send_show_command.

'''
from netmiko import ConnectHandler
import yaml


def send_show_command(device, command):
    result = ''
    for dev in device:
        with ConnectHandler(**dev) as ssh:
            ssh.enable()
            result += ssh.send_command(command) + '\n'
    return result


command = 'sh ip int br'
dev_name = 'devices.yaml'

with open(dev_name) as file:
    device = yaml.safe_load(file)

print(send_show_command(device, command))

