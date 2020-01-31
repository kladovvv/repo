# -*- coding: utf-8 -*-

'''
Задание 26.3a

Изменить класс IPAddress из задания 26.3.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

Для этого задания нет теста!
'''


class IPAddress:
    def __init__(self, ip_mask):
        self.prefix = ip_mask
        ip_address, mask = ip_mask.split('/')
        ip_list = ip_address.split('.')
        if len(ip_list) == 4:
            for i in ip_list:
                if int(i) in range(0, 256):
                    self.ip = ip_address
                else:
                    raise ValueError('Incorrect IPv4 address')
        else:
            raise ValueError('Incorrect IPv4 address')
        if int(mask) in range(8, 32):
            self.mask = int(mask)
        else:
            raise ValueError('Incorrect mask')

    def __str__(self):
        return f'IP address {self.prefix}'

    def __repr__(self):
        return f"IPAddress('{self.prefix}')"


if __name__ == '__main__':
    ip = IPAddress('10.1.255.1/24')
    input()

