# -*- coding: utf-8 -*-

'''
Задание 26.2

Добавить к классу CiscoTelnet из задания 25.2x поддержку работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.
Все исключения, которые возникли в менеджере контекста, должны генерироваться после выхода из блока with.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_26_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка
'''

import telnetlib
from textfsm import clitable
import time


class CiscoTelnet:
    def __init__(self, **params):
        self._output = ''
        self._device_ip = params['ip']
        self._telnet = telnetlib.Telnet(params['ip'])
        self._telnet.read_until(b'Username:')
        self._telnet.write(params['username'].encode('ascii') + b'\n')
        self._telnet.read_until(b'Password:')
        self._telnet.write(params['password'].encode('ascii') + b'\n')
        self._telnet.write(b'terminal length 0' + b'\n')
        self._telnet.read_until(b'#')
        self._telnet.read_until(b'#')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._telnet.close()

    def _write_line(self, string):
        self._telnet.write(string.encode('ascii') + b'\n')

    def send_show_command(self, show, parse=False, template='templates'):
        if parse is False:
            self._write_line(show)
            output = self._telnet.read_until(b'#').decode('utf-8')
            print(output)
        elif parse is True:
            result = []
            attributes = {'Command': show, 'Vendor': 'cisco_ios'}
            self._write_line(show)
            output = self._telnet.read_until(b'#').decode('utf-8')
            cli_t = clitable.CliTable(index_file='index', template_dir=template)
            cli_t.ParseCmd(output, attributes)
            for c in cli_t:
                result.append(dict(zip(list(cli_t.header), list(c))))
            print(result)

    def close(self):
        self._telnet.close()

    def send_config_commands(self, command, strict=False):
        self._telnet.write(b'conf t' + b'\n')
        if type(command) is str:
            self._telnet.write(command.encode('ascii') + b'\n')
            self._telnet.write(b'end' + b'\n')
            time.sleep(4)
            self._output = self._telnet.read_very_eager().decode('utf-8')
            self._print_output(command, strict)
        elif type(command) is list:
            for com in command:
                self._telnet.write(com.encode('ascii') + b'\n')
                time.sleep(4)
                self._output = self._telnet.read_very_eager().decode('utf-8')
                self._print_output(com, strict)
            self._telnet.write(b'end' + b'\n')

    def _print_output(self, command, strict):
        if strict is False:
            if "Invalid input detected" in self._output:
                print(f"При выполнении команды {command} на устройстве {self._device_ip} возникла ошибка -> Invalid input detected at '^' marker.")
            elif "Incomplete command" in self._output:
                print(f"При выполнении команды {command} на устройстве {self._device_ip} возникла ошибка -> Incomplete command.")
            elif "Ambiguous command" in self._output:
                print(f"При выполнении команды {command} на устройстве {self._device_ip} возникла ошибка -> Ambiguous command:  'i'")
            print(self._output)
        if strict is True:
            if "Invalid input detected" in self._output:
                raise ValueError(f"При выполнении команды {command} на устройстве {self._device_ip} возникла ошибка -> Invalid input detected at '^' marker.")
            elif "Incomplete command" in self._output:
                raise ValueError(f"При выполнении команды {command} на устройстве {self._device_ip} возникла ошибка -> Incomplete command.")
            elif "Ambiguous command" in self._output:
                raise ValueError(f"При выполнении команды {command} на устройстве {self._device_ip} возникла ошибка -> Ambiguous command:  'i'")
            else:
                print(self._output)


if __name__ == '__main__':
    r1_params = {'ip': '192.168.100.1',
                 'username': 'cisco',
                 'password': 'cisco',
                 'secret': 'cisco'}

    with CiscoTelnet(**r1_params) as r1:
        print('#' * 100)
        print(r1.send_show_command('sh clock'))
        raise ValueError('Возникла ошибка')

