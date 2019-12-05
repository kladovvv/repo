# -*- coding: utf-8 -*-
'''
Задание 20.3a

Создать функцию send_command_to_devices, которая отправляет
список указанных команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какие команды. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом каждой команды надо написать имя хоста и саму команду):

R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          87   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R1#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.30.0.1               -   aabb.cc00.6530  ARPA   Ethernet0/3.300
Internet  10.100.0.1              -   aabb.cc00.6530  ARPA   Ethernet0/3.100
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down
R3#sh ip route | ex -

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
O        10.1.1.1/32 [110/11] via 192.168.100.1, 07:12:03, Ethernet0/0
O        10.30.0.0/24 [110/20] via 192.168.100.1, 07:12:03, Ethernet0/0


Порядок команд в файле может быть любым.

Для выполнения задания можно создавать любые дополнительные функции, а также использовать функции созданные в предыдущих заданиях.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
'''
from netmiko import ConnectHandler
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import yaml
from os import remove
import logging


def send_command(device, command_list):
    result = []
    ip = device['ip']
    logging.info(f'START ===> datetime: {datetime.now().time()}, ip: {ip}')
    with ConnectHandler(**device) as ssh:
        for com in command_list:
            result.append(ssh.send_command(com))
    logging.info(f'STOP ===> datetime: {datetime.now().time()}, ip: {ip}')
    return result


def send_command_to_devices(devices, commands_dict, filename='output2.txt', limit=3):
    try:
        logging.info('Try to remove old file...')
        remove(filename)
        logging.info('Try to remove old file... success')
    except FileNotFoundError:
        logging.info('Nothing to remove')
    start_time = datetime.now()
    logging.info('Start: {}'.format(datetime.now()))
    numbers = ['R1', 'R2', 'R3']
    future_list = {}
    with ThreadPoolExecutor(max_workers=limit) as executor:
        for device, number in zip(devices, numbers):
            future_list[number] = executor.submit(send_command, device, commands_dict[device['ip']])
    with open(filename, 'a') as file:
        for (key1, value1), (key2, value2) in zip(future_list.items(), commands_dict.items()):
            for val1, val2 in zip(value1.result(), value2):
                file.write(key1 + '#' + val2 + '\n')
                file.write(val1 + '\n')
    logging.info('Stop: {}'.format(datetime.now()))
    print(datetime.now() - start_time)


with open('devices.yaml') as dev:
    dev_dict = yaml.safe_load(dev)
commands = {'192.168.23.2': ['sh ip int br', 'sh arp'],
            '192.168.23.3': ['sh arp'],
            '192.168.23.4': ['sh ip int br', 'sh ip route | ex -']}
logging.basicConfig(format='%(threadName)s %(name)s %(levelname)s: %(message)s', level=logging.INFO)
logging.getLogger("paramiko").setLevel(logging.WARNING)
send_command_to_devices(dev_dict, commands)




