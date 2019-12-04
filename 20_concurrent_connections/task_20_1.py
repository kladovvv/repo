# -*- coding: utf-8 -*-
'''
Задание 20.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.
'''
import subprocess
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def ping_ip(ip):
    res = subprocess.run(['ping', ip], stdout=subprocess.PIPE, shell=True, encoding='cp866')
    if res.returncode == 0 and 'TTL' in str(res):
        return True
    else:
        return False


def ping_ip_addresses(ip_list, limit=3):
    good = []
    bad = []
    start_time = datetime.now()
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(ping_ip, ip_list)
        for ip, res in zip(ip_list, result):
            if res:
                good.append(ip)
            else:
                bad.append(ip)
    print(datetime.now() - start_time)
    return good, bad


ip_good, ip_bad = ping_ip_addresses(['10.135.7.52', '10.135.7.54', '8.8.8.8', '1.1.1.1', '87.250.250.242', '9.9.9.9'],
                                    limit=6)
print('Список доступных IP: ', ip_good)
print('Список недоступных IP: ', ip_bad)