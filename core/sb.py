#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals
import re

__all__ = ["s", "b"]

def s(bytes, sep=" ", prefix="", suffix="", upper=True):
    '''
    return a unicode
    '''
    assert(isinstance(bytes, str))
    sep = unicode(sep)
    prefix = unicode(prefix)
    suffix = unicode(suffix)
    fmt = "%02X" if upper else "%02x"
    rets = []
    for c in bytes:
        rets.append("".join([prefix, fmt % (ord(c)), suffix]))
    r = sep.join(rets)
    return r

__HEX_STR_RE = re.compile(ur"^((?:0[xX])?([0-9a-fA-F]{2}\s*))+$")
__HEX_RM_RE = re.compile(ur"0[xX]|\s+")

def b(s):
    s = unicode(s)
    s = s.strip()
    if s == "":
        return b""
    if not __HEX_STR_RE.match(s):
        raise ValueError("this string cannot be converted to bytes")
    s = __HEX_RM_RE.sub("", s)
    hexs = []
    index = 0
    l = len(s)
    while index < l:
        hexs.append(s[index:index+2])
        index += 2
    return b"".join([chr(int(x, 16)) for x in hexs])


if __name__ == "__main__":
    x1 = "AA BB CC DD"
    x2 = b(x1)
    x3 = s(x2)
    print x1
    print x3
    a = b"".join([chr(x) for x in range(0x100)])
    print s(a)

