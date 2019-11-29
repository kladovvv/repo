# -*- coding: utf-8 -*-
'''
Задание 19.1a

Скопировать функцию send_show_command из задания 19.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется
при ошибке аутентификации на устройстве.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
'''
import netmiko
import yaml


def send_show_command(device, command):
    result = ''
    for dev in device:
        try:
            with netmiko.ConnectHandler(**dev) as ssh:
                ssh.enable()
                result += ssh.send_command(command) + '\n'
        except netmiko.ssh_exception.AuthenticationException as error:
            print(error)
    return result


command = 'sh ip int br'
dev_name = 'devices.yaml'

with open(dev_name) as file:
    device = yaml.safe_load(file)

print(send_show_command(device, command))