#!/usr/bin/env python
# -*- coding:utf8 -*-

__all__ = ["decode", "encode"]

def decode(string):
    if isinstance(string, str):
        decodes = ('gbk', 'utf8')
        for decode in decodes:
            try:
                s = string.decode(decode)
                return s
            except UnicodeDecodeError, e:
                continue
        raise Exception, "can not decode string"
    elif isinstance(string, unicode):
        return string
    else:
        raise TypeError, "string type must be in (str, uniocde)"

def encode(string):
    if isinstance(string, str):
        return string
    elif isinstance(string, unicode):
        decodes = ('gbk', 'utf8')
        for decode in decodes:
            try:
                s = string.encode(decode)
                return s
            except UnicodeDecodeError, e:
                continue
        raise Exception, "can not encode unicode string"
    else:
        raise TypeError, "string type must be in (str, uniocde)"

def main():
    pass

if __name__ == '__main__':
    main()

