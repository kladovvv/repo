# -*- coding: utf-8 -*-
import ipaddress
import subprocess


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


ip_good, ip_bad = ping_ip_addresses(['10.135.7.52', '10.135.7.54', '8.8.8.8', '1.1.1.1'])
print('Список доступных IP: ', ip_good)
print('Список недоступных IP: ', ip_bad)

# Пауза
input()