# -*- coding: utf-8 -*-
'''
Задание 21.1

Создать функцию generate_config.

Параметры функции:
* template - путь к файлу с шаблоном (например, "templates/for.txt")
* data_dict - словарь со значениями, которые надо подставить в шаблон

Функция должна возвращать строку с конфигурацией, которая была сгенерирована.

Проверить работу функции на шаблоне templates/for.txt и данных из файла data_files/for.yml.

'''
import yaml
from jinja2 import Environment, FileSystemLoader
import os


def generate_config(template, data_dict):
    temp_dir, temp = os.path.split(template)
    env = Environment(loader=FileSystemLoader(temp_dir), trim_blocks=True, lstrip_blocks=True)
    t = env.get_template(temp)
    with open(data_dict) as f:
        r_dict = yaml.safe_load(f)
    print(t.render(r_dict))


if __name__ == "__main__":
    generate_config('templates/for.txt', 'data_files/for.yml')
