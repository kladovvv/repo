# -*- coding: utf-8 -*-

'''
Задание 26.1

Изменить класс Topology из задания 25.1x.

Добавить метод, который позволит выполнять сложение двух объектов (экземпляров) Topology.
В результате сложения должен возвращаться новый экземпляр класса Topology.

Создание двух топологий:

In [1]: t1 = Topology(topology_example)

In [2]: t1.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [3]: topology_example2 = {('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
                             ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

In [4]: t2 = Topology(topology_example2)

In [5]: t2.topology
Out[5]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

Суммирование топологий:

In [6]: t3 = t1+t2

In [7]: t3.topology
Out[7]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R1', 'Eth0/6'): ('R9', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Проверка, что исходные топологии не изменились:

In [9]: t1.topology
Out[9]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [10]: t2.topology
Out[10]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}
'''


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def __add__(self, other):
        sum_topology = {}
        sum_topology.update(self.topology)
        sum_topology.update(other.topology)
        return Topology(sum_topology)

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

topology_example2 = {('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
                     ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

t1 = Topology(topology_example)
t2 = Topology(topology_example2)
t3 = t1 + t2
print(t1.topology)
print('#' * 100)
print(t2.topology)
print('#' * 100)
print(t3.topology)
input()