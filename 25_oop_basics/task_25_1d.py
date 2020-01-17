# -*- coding: utf-8 -*-

'''
Задание 25.1d

Изменить класс Topology из задания 25.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще нет в топологии
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение "Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


'''


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        result = {}
        for k, v in topology_dict.items():
            if v not in result.keys() and k not in result.values():
                result.update({k: v})
        return result

    def delete_link(self, link_1side, link_2side):
        if (link_1side, link_2side) in self.topology.items():
            del self.topology[link_1side]
            try:
                del self.topology[link_2side]
            except KeyError:
                pass
        elif (link_2side, link_1side) in self.topology.items():
            del self.topology[link_2side]
        else:
            print('Такого линка нет')

    def delete_node(self, node):
        result = {}
        flag = 0
        for k, v in self.topology.items():
            key1 = k[0]
            value1 = v[0]
            if node == key1 or node == value1:
                flag += 1
            else:
                result[k] = v
        if flag == 0:
            print('Такого устройства нет')
        self.topology = result

    def add_link(self, link_1side, link_2side):
        if (link_1side, link_2side) in self.topology.items() or (link_2side, link_1side) in self.topology.items():
            print('Такое соединение существует')
        elif link_1side in self.topology.keys() or link_2side in self.topology.keys():
            print('Соединение с одним из портов существует')
        elif link_1side in self.topology.values() or link_2side in self.topology.values():
            print('Соединение с одним из портов существует')
        else:
            self.topology[link_1side] = link_2side


topology_example = {('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
                    ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
                    ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
                    ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
                    ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
                    ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
                    ('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
                    ('SW1', 'Eth0/2'): ('R2', 'Eth0/0'),
                    ('SW1', 'Eth0/3'): ('R3', 'Eth0/0')}

top = Topology(topology_example)
print(top)
