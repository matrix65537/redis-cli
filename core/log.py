#!/usr/bin/python
#coding:utf8

import sys
import time
import argparse
import consolecolor as ccc

__all__ = ["Log", "verbose", "develop", "debug", "info", "warning", "error", "set_log_level", "set_log_file", "get_log_level", "get_log_file"]

################################################################################

class Log(object):

    NONE        = 0
    ERROR       = 1
    WARNING     = 2
    INFO        = 3
    DEBUG       = 4
    DEVELOP     = 5
    VERBOSE     = 6

    def __init__(self, level = INFO):
        self.__stdout = sys.stdout
        self.__orig_color = ccc.get_color()
        self.__level = level
        self.__show_time_flag = False
        self.__fobj = self.__stdout

    def set_log_file(self, fileobj):
        self.__fobj = fileobj

    def get_log_file(self, fileobj):
        return self.__fobj

    def set_log_level(self, level):
        self.__level = level

    def get_log_level(self):
        return self.__level

    def set_show_time_flag(self, flag):
        self.__show_time_flag = flag

    def __print(self, msg_color_pairs):
        if self.__fobj:
            fmt = "%Y-%m-%d %X"
            timeval = time.strftime(fmt, time.localtime())
            for msg, color in msg_color_pairs:
                if self.__fobj == self.__stdout:
                    ccc.set_color(color)
                if self.__show_time_flag:
                    self.__fobj.write(timeval + '\n')
                self.__fobj.write(msg)
                self.__fobj.flush()
                if self.__fobj == self.__stdout:
                    ccc.set_color(self.__orig_color)

    def __print_msg(self, level, pre, msg, color):
        if self.__level >= level:
            #self.__print([(pre + "\n", color)])
            self.__print([(msg + "\n", color)])

    def develop(self, msg):
        self.__print_msg(Log.DEVELOP, "[DEVP]", msg, ccc.SKYBLUE)

    def debug(self, msg):
        self.__print_msg(Log.DEBUG, "[DBUG]", msg, ccc.GREEN)

    def info(self, msg):
        self.__print_msg(Log.INFO, "[INFO]", msg, ccc.get_color())

    def warning(self, msg):
        self.__print_msg(Log.WARNING, "[WARN]", msg, ccc.YELLOW)

    def error(self, msg):
        self.__print_msg(Log.ERROR, "[ERRO]", msg, ccc.RED)

    def verbose(self, msg):
        self.__print_msg(Log.VERBOSE, "[VERB]", msg, ccc.PURPLE)

_log_obj = Log()

################################################################################

def set_log_file(fileobj):
    _log_obj.set_log_file(fileobj)

def get_log_file():
    return _log_obj.get_log_file()

def set_log_level(level):
    _log_obj.set_log_level(level)

def get_log_level():
    return _log_obj.get_log_level()

def develop(msg):
    _log_obj.develop(msg)

def debug(msg):
    _log_obj.debug(msg)

def info(msg):
    _log_obj.info(msg)

def warning(msg):
    _log_obj.warning(msg)

def error(msg):
    _log_obj.error(msg)

def verbose(msg):
    _log_obj.verbose(msg)

################################################################################

def main():
    msg = "The quick brown fox jumps over a lazy dog"
    develop(msg)
    debug(msg)
    info(msg)
    warning(msg)
    error(msg)

################################################################################

if __name__ == '__main__':
    main()

