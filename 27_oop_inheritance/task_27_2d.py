# -*- coding: utf-8 -*-

'''
Задание 27.2d

Дополнить класс MyNetmiko из задания 27.2c или задания 27.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен работать точно так же как метод send_config_set в netmiko.

Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_27_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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

    def send_config_set(self, config_commands=None, ignore_errors=True, **kwargs):
        if ignore_errors:
            return super().send_config_set(config_commands, **kwargs)
        else:
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
    result = r1.send_config_set(['int loo2', 'ip add 10.0.1 255.255.255.255', 'delay 1000'], ignore_errors=True)
    print(result)
    r1.disconnect()
