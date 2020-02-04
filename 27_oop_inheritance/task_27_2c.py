# -*- coding: utf-8 -*-

'''
Задание 27.2c

Проверить, что метод send_command класса MyNetmiko из задания 27.2b, принимает дополнительные аргументы (как в netmiko), кроме команды.

Если возникает ошибка, переделать метод таким образом, чтобы он принимал любые аргументы, которые поддерживает netmiko.


In [2]: from task_27_2c import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br', strip_command=False)
Out[4]: 'sh ip int br\nInterface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip int br', strip_command=True)
Out[5]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

'''
import netmiko


class ErrorInCommand(Exception):
    pass


class MyNetmiko(netmiko.cisco.cisco_ios.CiscoIosBase):
    def __init__(self, **kwargs):
        self._ip = kwargs['ip']
        super().__init__(**kwargs)
        self.enable()

    def send_command(self, command_string, **kwargs):
        temp_result = super().send_command(command_string, **kwargs)
        output = self._check_error_in_command(command_string, temp_result)
        return output

    def send_config_set(self, config_commands=None, **kwargs):
        output = str()
        if isinstance(config_commands, list):
            for cc in config_commands:
                temp_result = super().send_config_set(cc, exit_config_mode=False, **kwargs)
                output += self._check_error_in_command(cc, temp_result)
        else:
            temp_result = super().send_config_set(config_commands, **kwargs)
            output = self._check_error_in_command(config_commands, temp_result)
        super().exit_config_mode()
        return output

    def _check_error_in_command(self, command_string, temp_result):
        if 'Invalid input detected' in temp_result:
            raise ErrorInCommand(f'''При выполнении команды {command_string} на устройстве {self._ip} возникла ошибка "Invalid input detected at '^' marker."''')
        elif 'Incomplete command' in temp_result:
            raise ErrorInCommand(f'''При выполнении команды {command_string} на устройстве {self._ip} возникла ошибка "Incomplete command"''')
        elif 'Ambiguous command' in temp_result:
            raise ErrorInCommand(f'''При выполнении команды {command_string} на устройстве {self._ip} возникла ошибка "Ambiguous command"''')
        else:
            return temp_result


if __name__ == '__main__':
    device_params = {
        'device_type': 'cisco_ios',
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'
    }
    r1 = MyNetmiko(**device_params)
    result = r1.send_command('sh ip int br', strip_command=False)
    print(result)
    r1.disconnect()
