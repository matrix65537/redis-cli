#!/usr/bin/python
#coding:utf8

from sb import s, b

__debug_mode = False

__functioni_level = 0

__all__ = ["set_debug_mode", "get_debug_mode", "debug_info", "ds", "get_dump_string", "all_print_string", "set_binary_mode"]

def set_debug_mode(debug_mode):
    global __debug_mode
    __debug_mode = debug_mode

def get_debug_mode():
    return __debug_mode

def debug_info(info = "DEBUG_INFO"):
    def __f1(f):
        def __f2(*args, **kw):
            global __functioni_level
            if get_debug_mode():
                __functioni_level += 1
                argcount = f.func_code.co_argcount
                co_varnames = f.func_code.co_varnames
                defaults = f.func_defaults or ()
                len_arg = len(args)
                len_default = len(defaults)
                largs = args
                if len_arg < argcount:
                    largs += defaults[len_arg - argcount:]
                largs = list(largs)
                for k, v in kw.items():
                    for i in range(len(co_varnames)):
                        if k == co_varnames[i]:
                            largs[i] = v
                            break
                rjust_length = 0x10
                print "%s>> %s : [%s] (level = %d)" %(info, "function".rjust(rjust_length), f.__name__, __functioni_level)
                for i, v in enumerate(largs):
                    if isinstance(v, str):
                        length = len(v)
                        msg = "%s>> %s : [0x%04X] %s" %(info, co_varnames[i].rjust(rjust_length), length, s(v, ''))
                    else:
                        msg = "%s>> %s : %s" %(info, co_varnames[i].rjust(rjust_length), str(v))
                    print msg
            O = f(*args, **kw)
            if get_debug_mode():
                if isinstance(O, str):
                    length = len(O)
                    print "%s>> %s : [0x%04X] %s" %(info, "return".rjust(rjust_length), length, s(O, ''))
                elif isinstance(O, (list, tuple)):
                    for i, v in enumerate(O):
                        if isinstance(v, str):
                            length = len(v)
                            msg = "%s>> %s : [0x%04X] %s" %(info, "return".rjust(rjust_length), length, s(v, ''))
                        else:
                            msg = "%s>> %s : %s" %(info, "return".rjust(rjust_length), str(v))
                        print msg
                else:
                    msg = "%s>> %s : " %(info, "return".rjust(rjust_length))
                    print msg, type(O), O
                __functioni_level -= 1
                print '_' * 80
            return O
        return __f2
    return __f1

PRINT_STRING = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\"()*+,-./:;<=>?@[\\]^_`{|}~ '

def all_print_string(bytes):
    for x in bytes:
        if x not in PRINT_STRING:
            return False
    return True

def ds(bytes, include_ascii = False, include_addr = False, colsize = 0x10):
    assert(isinstance(bytes, str))
    length = len(bytes)
    i = 0
    L = []
    rownum = 0
    while True:
        if i >= length:
            break
        T = []
        if include_addr:
            T.append("%04X: "  %(rownum * colsize))
        for j in range(i, i + colsize):
            if j < length:
                T.append("%02X " %ord(bytes[j]))
            else:
                T.append("   ")
            if j % colsize == (colsize / 2 - 1):
                T.append(" ")
        if include_ascii:
            T.append("\t")
            for j in range(i, i + colsize):
                if j < length:
                    if bytes[j] in PRINT_STRING:
                        T.append(bytes[j])
                    else:
                        T.append(".")
                else:
                    T.append("  ")
        L.append("".join(T))
        i += colsize
        rownum += 1
    return "\n".join(L)

def get_dump_string(name, data):
    output_str = '[%s]\n%s\n' %(name, ds(data, include_ascii = True))
    return output_str

def set_binary_mode():
    try:
        import msvcrt
        import sys
        import os
        stdin_fd = sys.stdin.fileno()
        stdout_fd = sys.stdout.fileno()
        stderr_fd = sys.stderr.fileno()
        if not os.isatty(stdin_fd):
            msvcrt.setmode(stdin_fd,os.O_BINARY)
        if not os.isatty(stdout_fd):
            msvcrt.setmode(stdout_fd,os.O_BINARY)
        if not os.isatty(stderr_fd):
            msvcrt.setmode(stderr_fd,os.O_BINARY)
    except ImportError:
        pass

def main():
    print ds("var1", '\xAB' * 0x20)
    print ds("var2", '\xAB' * 0x100)

if __name__ == '__main__':
    main()
