# -*- coding: utf-8 -*-

'''
Задание 25.2c

Скопировать класс CiscoTelnet из задания 25.2b и изменить метод send_config_commands добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать исключение ValueError
* strict=False значит, что при обнаружении ошибки, надо только вывести на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).
Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_25_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'i']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "i" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "i"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#i
% Ambiguous command:  "i"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

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

    r1 = CiscoTelnet(**r1_params)
    print('#' * 100)
    r1.send_config_commands(['logging 0255.255.1', 'logging', 'router i'])
    print('#' * 100)
    r1.close()

