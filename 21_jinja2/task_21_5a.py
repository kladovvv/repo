# -*- coding: utf-8 -*-
'''
Задание 21.5a

Создать функцию configure_vpn, которая использует шаблоны из задания 21.5 для настройки VPN на маршрутизаторах на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству
* dst_device_params - словарь с параметрами подключения к устройству
* src_template - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* dst_template - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов и данных на каждом устройстве.
Функция возвращает вывод с набором команд с двух марушртизаторов (вывод, которые возвращает send_config_set).

При этом, в словаре data не указан номер интерфейса Tunnel, который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel, взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 9.
И надо будет настроить интерфейс Tunnel 9.

Для этого задания нет теста!
'''

from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler


def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True, lstrip_blocks=True)
    a_temp = env.get_template(src_template)
    b_temp = env.get_template(dst_template)
    print(show_connect(src_device_params, 'sh ip int br'))
    print(show_connect(dst_device_params, 'sh ip int br'))


def show_connect(device_params, sh_comm):
    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_command(sh_comm)
    return result


def set_connect(device_params, set_comm):
    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_config_set(set_comm)
    return result


data = {
    'tun_num': None,
    'wan_ip_1': '192.168.100.1',
    'wan_ip_2': '192.168.100.2',
    'tun_ip_1': '10.0.1.1 255.255.255.252',
    'tun_ip_2': '10.0.1.2 255.255.255.252'
}

src_device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.23.2',
    'username': 'cisco',
    'password': 'cisco'
}

dst_device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.23.3',
    'username': 'cisco',
    'password': 'cisco'
}


configure_vpn(src_device,
              dst_device,
              'gre_ipsec_vpn_1.txt',
              'gre_ipsec_vpn_2.txt',
              data)
