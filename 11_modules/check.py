# -*- coding: utf-8 -*-

def parse_cdp_neighbors(command_output):
    command_output_list = command_output.split('\n')
    connect = {}
    for string in command_output_list:
        if string and '>' in string:
            local_device = string.split('>')[0]
        if string and 'Eth' in string:
            remote_device, local_int, local_port, *args, remote_int, remote_port = string.split()
            connect[(local_device, local_int + local_port)] = (remote_device, remote_int + remote_port)
    return connect

if __name__ == "__main__":
    file = open('sh_cdp_n_sw1.txt', 'r')
    print(parse_cdp_neighbors(file.read()))
    file.close()