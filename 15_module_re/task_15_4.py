# -*- coding: utf-8 -*-
'''
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
'''
import re


def get_ints_without_description(filename):
    intf_desc = []
    intf = []
    with open(filename) as file:
        for match in re.finditer('interface (?P<intf>\S+)\s+description', file.read()):
            intf_desc.append(match.group('intf'))
        file.seek(0)
        for f in file:
            match2 = re.search('interface (?P<intf2>\S+[\d+/])', f)
            if match2 and not match2.group('intf2') in intf_desc:
                intf.append(match2.group('intf2'))
    return intf


print(get_ints_without_description('config_r1.txt'))
