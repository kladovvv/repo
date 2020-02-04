# -*- coding: utf-8 -*-

'''
Задание 27.2b

Дополнить класс MyNetmiko из задания 27.2a.

Переписать метод send_config_set netmiko, добавив в него проверку на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает вывод команд.

In [2]: from task_27_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

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
    result = r1.send_config_set('logging 10.10.10')
    print(result)
    r1.disconnect()
