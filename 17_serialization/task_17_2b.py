# -*- coding: utf-8 -*-
'''
Задание 17.2b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно, чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии, но и удалять дублирующиеся соединения (их лучше всего видно на схеме, которую генерирует draw_topology).

Проверить работу функции на файле topology.yaml. На основании полученного словаря надо сгенерировать изображение топологии с помощью функции draw_topology.
Не копировать код функции draw_topology.

Результат должен выглядеть так же, как схема в файле task_17_2b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть дублирующихся линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

'''
import yaml
from pprint import pprint
from draw_network_graph import draw_topology


def transform_topology(yaml_filename):
    draw_dict = {}
    with open(yaml_filename) as top:
        topology = yaml.safe_load(top)
        for k1, v1 in topology.items():
            for k2, v2 in v1.items():
                if not set(v2.items()) & set(draw_dict.keys()):
                    draw_dict.update({(k1, k2): (k3, v3) for k3, v3 in v2.items()})
    return draw_dict


pprint(transform_topology('topology.yaml'))
draw_topology(transform_topology('topology.yaml'), out_filename='my_17b_topology')