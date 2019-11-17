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


def transform_topology(yaml_filename):
    draw_dict = {}
    with open(yaml_filename) as top:
        topology = yaml.safe_load(top)
        for key, value in topology.items():
            for value_key, value_value in value.items():
                for value_value_key, value_value_value in value_value.items():
                    temp_dict = {(key, value_key): (value_value_key, value_value_value)}
                    draw_dict.update(temp_dict)
    d = {}
    for k in draw_dict.keys():
        for v in draw_dict.values():
            if k == v:
                break
            else:
    return draw_dict


pprint(transform_topology('topology.yaml'))
