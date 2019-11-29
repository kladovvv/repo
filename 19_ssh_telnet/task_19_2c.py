# -*- coding: utf-8 -*-
'''
Задание 19.2c

Скопировать функцию send_config_commands из задания 19.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка,
спросить пользователя надо ли выполнять остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию, поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

'''
import netmiko
import yaml
import re
from pprint import pprint


def send_config_commands(device, config_commands, verbose=True):
    good = {}
    bad = {}
    if verbose:
        print('Подключаюсь к', device['ip'], '...')
    with netmiko.ConnectHandler(**device) as ssh:
        for command in config_commands:
            res = ssh.send_config_set(command)
            match = re.search(r'(Invalid input detected at.* marker.|Incomplete command.|Ambiguous command:)', res)
            if match:
                bad[command] = res
                print(f'''Команда "{command}" выполнилась с ошибкой "{match.group(1)}" на устройстве {device['ip']}''')
                q = input('Продолжать выполнять команды? [y]/n: ')
                if q == 'n' or q == 'no':
                    return good, bad
            else:
                good[command] = res
    return good, bad


# списки команд с ошибками и без:
commands_with_errors = ['logging 0255.255.1', 'logging', 'i']
correct_commands = ['logging buffered 20010', 'ip http server']
commands = commands_with_errors + correct_commands

dev_file = 'devices.yaml'
with open(dev_file) as file:
    devices = yaml.safe_load(file)
r1, r2, r3 = devices
result = send_config_commands(r1, commands)
pprint(result, width=120)
