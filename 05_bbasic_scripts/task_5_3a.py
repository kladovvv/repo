# -*- coding: utf-8 -*-
'''
Задание 5.3a

Дополнить скрипт из задания 5.3 таким образом, чтобы, в зависимости от выбранного режима,
задавались разные вопросы в запросе о номере VLANа или списка VLANов:
* для access: 'Введите номер VLAN:'
* для trunk: 'Введите разрешенные VLANы:'

Ограничение: Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if и циклов for/while.
'''

access_template = [
    'switchport mode access', 'switchport access vlan {}',
    'switchport nonegotiate', 'spanning-tree portfast',
    'spanning-tree bpduguard enable'
]
access_template = '\n'.join(access_template)


trunk_template = [
    'switchport trunk encapsulation dot1q', 'switchport mode trunk',
    'switchport trunk allowed vlan {}'
]
trunk_template = '\n'.join(trunk_template)

ty = input('введите режим работы интерфейса (access/trunk): ')
type_number = input('введите тип и номер интерфейса: ')

t = {'access': 'Введите номер VLAN: ',
    'trunk': 'Введите разрешенные VLANы: '}

vlan = input(t[ty])

dic = {'access': 'interface {}\n' + access_template,
'trunk': 'interface {}\n' + trunk_template}

print(dic[ty].format(type_number, vlan))