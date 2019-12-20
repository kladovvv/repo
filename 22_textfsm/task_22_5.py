# -*- coding: utf-8 -*-
'''
Задание 22.5

Создать функцию send_and_parse_command_parallel.

Функция send_and_parse_command_parallel должна запускать в параллельных потоках функцию send_and_parse_show_command из задания 22.4.

В этом задании надо самостоятельно решить:
* какие параметры будут у функции
* что она будет возвращать


Теста для этого задания нет.
'''
import textfsm
import yaml
import netmiko
import os
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat


logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.basicConfig(
    format='%(threadName)s: %(message)s',
    level=logging.INFO)


def send_and_parse_show_command(device_dict, command, templates_path):
    logging.info('START:')
    logging.info(datetime.now())
    with netmiko.ConnectHandler(**device_dict) as ssh:
        output = ssh.send_command(command)
    with open(templates_path) as template:
        fsm = textfsm.TextFSM(template)
        data = fsm.ParseTextToDicts(output)
    logging.info('STOP:')
    logging.info(datetime.now())
    return data


with open('devices.yaml') as dev:
    devices = yaml.safe_load(dev)
command = 'sh ip int br'
templates = os.path.join(os.getcwd(), 'templates', 'sh_ip_int_br.template')


def send_and_parse_command_parallel(devices, command, templates):
    with ThreadPoolExecutor(max_workers=3) as executor:
        result = executor.map(send_and_parse_show_command, devices, repeat(command), repeat(templates))
        for d, o in zip(devices, result):
            print(d['ip'], '\n', o)


start_time = datetime.now()
send_and_parse_command_parallel(devices, command, templates)
print(datetime.now() - start_time)