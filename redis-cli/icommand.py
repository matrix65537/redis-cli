#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import argparse
from scplib import *

class CmdException(Exception):
    pass

class CmdExitException(Exception):
    pass

class CmdParser(argparse.ArgumentParser):

    def exit(self, status=0, message=None):
        if message:
            raise CmdExitException, message

class Command(object):

    def __init__(self):
        pass

    def init(self, cmd_name):
        self.__cmd_name = cmd_name
        self.__parser = CmdParser(prog = self.__cmd_name, formatter_class = argparse.ArgumentDefaultsHelpFormatter, add_help = False)

    def get_name(self):
        return self.__cmd_name

    def add_args(self):
        pass

    def get_parser(self):
        return self.__parser

    def perform(self, argv):
        pass

def dump_tlv(bytes):
    tlvobj_list = parse_tlv(bytes)
    for tlvobj in tlvobj_list:
        debug(tlvobj.get_dump_string())

def strip_filename(filename):
    '''过滤掉文件名称包含的双引号'''
    if filename.startswith('"'):
        filename = filename[1:]
    if filename.endswith('"'):
        filename = filename[:-1]
    return filename

################################################################################

def output_set(d, ljust_size, col_size = 0x04):
    if isinstance(d, dict):
        keys = d.keys()
    elif isinstance(d, (list, tuple)):
        keys = list(d)
    else:
        pass
    keys.sort()
    length = len(keys)
    for i in range(length):
        key_info = "%02d: %s" %(i + 1, keys[i])
        key_info = key_info.ljust(ljust_size)
        print key_info,
        if i % col_size == (col_size - 1):
            print
    if length % col_size != 0x00:
        print
