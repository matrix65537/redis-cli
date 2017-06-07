#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
from scplib import *
from icommand import CmdException

class RedisException(CmdException):
    pass

class RedisClient(object):

    def __init__(self):
        pass

    def connect(self, ip = '127.0.0.1', port = 6379):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.setblocking(True)
        self.server_addr = (ip, port)
        client_sock.connect(self.server_addr)
        self.client_sock = client_sock

    def encode_cmd(self, cell_list):
        rlist = []
        rlist.append("*%d" %(len(cell_list)))
        for cell in cell_list:
            rlist.append("$%d" %(len(cell)))
            rlist.append(cell)
        rlist.append(b'\x0D\x0A')
        cmd = '\r\n'.join(rlist)
        return cmd

    def read_util_DA(self):
        flag_D = False
        flag_A = False
        rlist = []
        while True:
            if flag_D and flag_A:
                break
            c = self.client_sock.recv(1)
            rlist.append(c)
            if c == b'\x0D':
                flag_D = True
                c = self.client_sock.recv(1)
                rlist.append(c)
                if c == b'\x0A':
                    flag_A = True
                else:
                    flag_D = False
        data = b''.join(rlist)
        return data

    def read_dollar(self):
        data = self.read_util_DA()
        length = int(data[:-2])
        data2 = self.client_sock.recv(length + 2)
        return data + data2

    def read_x(self):
        rlist = []
        data = self.read_util_DA()
        rlist.append(data)
        length = int(data[:-2])
        for i in range(length):
            c = self.client_sock.recv(1)
            assert(c == b'$')
            rlist.append(c)
            cell = self.read_dollar()
            rlist.append(cell)
        rsp = b''.join(rlist)
        return rsp


    def read_rsp(self):
        c = self.client_sock.recv(1)
        if c in (b'+', b'-'):
            data = self.read_util_DA()
        elif c == b'$':
            data = self.read_dollar()
        elif c == b':':
            data = self.read_util_DA()
        elif c == b'*':
            data = self.read_x()
        else:
            raise RedisException("unexpected response")
            data = b""
        return data

    def transmit(self, cell_list):
        cmd = self.encode_cmd(cell_list)
        self.client_sock.send(cmd)
        rsp = self.read_rsp()
        return rsp

def main():
    pass

if __name__ == '__main__':
    main()

