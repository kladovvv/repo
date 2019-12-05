# -*- coding: utf-8 -*-
'''
Задание 20.2

Создать функцию send_show_command_to_devices, которая отправляет
одну и ту же команду show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
'''
import yaml
from concurrent.futures import ThreadPoolExecutor
import netmiko
from datetime import datetime
from itertools import repeat


def send_command(device, command):
    with netmiko.ConnectHandler(**device) as ssh:
        result = ssh.send_command(command)
    return result


def send_show_command_to_devices(devices, command, filename='output.txt', limit=3):
    start_time = datetime.now()
    number = ['R1', 'R2', 'R3']
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(send_command, devices, repeat(command))
    for device, res, num in zip(devices, result, number):
        with open(filename, 'a') as f:
            f.write(num + command + '\n')
            f.write(res + '\n')
    print(datetime.now() - start_time)


with open('devices.yaml') as file:
    dev = yaml.safe_load(file)
com = 'show ip int br'
send_show_command_to_devices(dev, com)