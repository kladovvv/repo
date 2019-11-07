# -*- coding: utf-8 -*-
import ipaddress
import subprocess
from tabulate import tabulate


def ping_ip_addresses(ip_addresses):
    enable = []
    disable = []
    for ip in ip_addresses:
        try:
            ipaddress.ip_address(ip)
            result = subprocess.run(['ping', ip], stdout=subprocess.PIPE, shell=True, encoding='cp866')
            if result.returncode == 0 and 'TTL' in str(result):
                enable.append(ip)
            else:
                disable.append(ip)
        except ValueError:
            print(ip, '- Wrong IP')
            continue
    return enable, disable


def convert_ranges_to_ip_list(list_of_range_ip):
    new_list_of_range_ip = []
    for range_ip in list_of_range_ip:
        range_ip_list = range_ip.split('-')
        if len(range_ip_list) == 1:
            new_list_of_range_ip.append(range_ip)
        else:
            try:
                ipaddress.ip_address(range_ip_list[1])
                for ip in range(int(ipaddress.ip_address(range_ip_list[0])), int(ipaddress.ip_address(range_ip_list[1])) + 1):
                    new_list_of_range_ip.append(str(ipaddress.ip_address(ip)))
            except ValueError:
                if range_ip_list[1].isdigit():
                    octets = range_ip_list[0].split('.')
                    octets[3] = range_ip_list[1]
                    for ip in range(int(ipaddress.ip_address(range_ip_list[0])), int(ipaddress.ip_address('.'.join(octets))) + 1):
                        new_list_of_range_ip.append(str(ipaddress.ip_address(ip)))
                else:
                    print("Неверно задан один из диапазонов")
                    continue
    return new_list_of_range_ip


def print_ip_table(reach, unreach):
    columns = ['reachable', 'unreachable']
    list1 = []
    for c in columns:
        if c == 'reachable':
            for r in reach:
                list1.append({c: r})
        elif c == 'unreachable':
            for u in unreach:
                list1.append({c: u})
    print(list1)
    return print(tabulate(list1, headers='keys'))


list_of_ip = ['10.135.7.52-10.135.7.53', '10.135.7.30-31', '8.8.8.8']
print(convert_ranges_to_ip_list(list_of_ip))
ip_good, ip_bad = ping_ip_addresses(convert_ranges_to_ip_list(list_of_ip))
print_ip_table(ip_good, ip_bad)

ccc = ['reachable', 'unreachable']
ppp = [('1.1.1.1', '8.8.8.8'), ('2.2.2.2', '3.3.3.3'), ('7.7.7.7',), ('6.6.6.6',)]
print(tabulate(ppp, headers=ccc))
input()