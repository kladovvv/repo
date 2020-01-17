# -*- coding: utf-8 -*-

'''
Задание 25.2b

Скопировать класс CiscoTelnet из задания 25.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного режима или список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_25_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

'''
import telnetlib
from textfsm import clitable
import time


class CiscoTelnet:
    def __init__(self, **params):
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

    def send_config_commands(self, command):
        self._telnet.write(b'conf t' + b'\n')
        if type(command) is str:
            self._telnet.write(command.encode('ascii') + b'\n')
            self._telnet.write(b'end' + b'\n')
            time.sleep(4)
            output = self._telnet.read_very_eager().decode('utf-8')
            print(output)
        elif type(command) is list:
            for com in command:
                self._telnet.write(com.encode('ascii') + b'\n')
            self._telnet.write(b'end' + b'\n')
            time.sleep(4)
            output = self._telnet.read_very_eager().decode('utf-8')
            print(output)


if __name__ == '__main__':
    r1_params = {'ip': '192.168.100.1',
                 'username': 'cisco',
                 'password': 'cisco',
                 'secret': 'cisco'}

    r1 = CiscoTelnet(**r1_params)
    print('#' * 100)
    r1.send_config_commands('logging 10.1.1.1')
    print('#' * 100)
    r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
    print('#' * 100)
    r1.close()
