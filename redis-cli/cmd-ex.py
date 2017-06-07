#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

__copyright__ = '''If you meet some problems, please contact guobaorui4365@126.com
Copyright (c) 2017-2027 Two Prime Numbers.
All Rights Reserved.
'''
__version__ = "version: 2.6.5"


import os
import os.path
import sys
import re
import argparse
from scplib import *

from iplugin import Plugin
from icommand import *
from state import *

################################################################################

DEFAULT_PLUGIN_NAME = ""

_cmd_dict = {}
_var_dict = {}

set_var_dict(_var_dict)

# all plugin included in this dict that are already registered when init.
_plugin_dict = {}
# current plugin name and object
_plugin_name = DEFAULT_PLUGIN_NAME
_plugin_object = None

_completer = None

################################################################################

import redisplugin

# you can write a plugin, and add to this modules list.
_modules = [redisplugin]

def register_plugins():
    register(_plugin_dict)
    for module in _modules:
        module.register(_plugin_dict)

################################################################################

def find_cmd(cmd_name):
    cmd_object_list = []
    #full match
    if cmd_name in _cmd_dict:
        cmd_object = _cmd_dict[cmd_name]
        cmd_object_list.append(cmd_object)
    #search partion math
    else:
        for k, v in _cmd_dict.items():
            split_tuple = k.split('-')
            T = cmd_name.split('-')
            if len(T) <= len(split_tuple):
                flag = True
                for i in range(len(T)):
                    if not split_tuple[i].startswith(T[i]):
                        flag = False
                        break
                if flag:
                    cmd_object_list.append(v)
    if len(cmd_object_list) == 0:
        # use re
        for k, v in _cmd_dict.items():
            try:
                r = re.compile(k)
                if r.match(cmd_name):
                    cmd_object_list.append(v)
                    break
            except:
                continue
    return cmd_object_list

################################################################################

def init_plugin_object(plugin_object):
    cmd_dict = {}
    for cmd_name, cmd_class in plugin_object.get_cmd_dict().items():
        cmd_object = cmd_class()
        cmd_object.init(cmd_name)
        cmd_object.add_args()
        cmd_dict[cmd_name] = cmd_object
    return cmd_dict

################################################################################

class Completer(object):
    def __init__(self):
        self.matches = []
        self.ext_matches = []

    def set_ext_matches(self, ext_matches):
        self.ext_matches = ext_matches

    def cmd_matches(self, text):
        matches = []
        #第一类为查找到的命令
        cmd_object_list = find_cmd(text)
        for cmd_object in cmd_object_list:
            matches.append(cmd_object.get_name())

        #当前目录的文件
        for file_dir in os.listdir('.'):
            if file_dir.startswith(text):
                matches.append(file_dir)

        #加上扩展提示
        for v in self.ext_matches:
            if v.startswith(text):
                matches.append(v)

        self.matches = matches

    def __call__(self, text, state):
        text = ed.decode(text)
        if state == 0:
            self.cmd_matches(text)
        try:
            return self.matches[state]
        except IndexError:
            return None

try:
    import readline
except ImportError:
    readline = None

HOMEDIR = os.environ.get("HOME")
if not HOMEDIR:
    HOMEDIR = os.environ.get("USERPROFILE", ".")

def init_readline():
    if not readline:
        return
    global _completer
    _completer = Completer()
    readline.set_completer(_completer)
    readline.parse_and_bind('tab: complete')
    try:
        readline.read_history_file(HOMEDIR + "/.redis-cli-hist")
    except IOError:
        pass
    def on_exit():
        readline.write_history_file(HOMEDIR + "/.redis-cli-hist")
    import atexit
    atexit.register(on_exit)

################################################################################

class CommandApp(Command):
    def add_args(self):
        self.get_parser().add_argument('name', nargs = '?', help='switch plugin')

    def perform(self, argv):
        global _plugin_name, _plugin_object
        global _cmd_dict
        ns = self.get_parser().parse_args(argv[1:])
        if ns.name:
            name = ns.name
            if name not in _plugin_dict:
                raise CmdException, "plugin name invalid"
            _plugin_name = name
            _plugin_object = _plugin_dict[_plugin_name]

            base_plugin_object = _plugin_dict[DEFAULT_PLUGIN_NAME]
            _cmd_dict = init_plugin_object(base_plugin_object)
            _cmd_dict.update(init_plugin_object(_plugin_object))

            _var_dict.update(_ivar_dict)
            _var_dict.update(_plugin_object.get_var_dict())

            _completer.set_ext_matches(_plugin_object.get_ext_matches())
        else:
            # if the name is empty, then list all plugins's name
            keys = _plugin_dict.keys()
            keys.sort()
            for i in range(len(keys)):
                if keys[i]:
                    debug("%02d : %s" %(i, keys[i]))


class CommandHelp(Command):

    def add_args(self):
        self.get_parser().add_argument('cmd', nargs = '*', help='show command help info')

    def perform(self, argv):
        ns = self.get_parser().parse_args(argv[1:])
        cmd = ns.cmd
        if len(cmd) == 0:
            output_set(_cmd_dict, 30, 0x02)
        elif len(cmd) == 1:
            cmd_object_list = find_cmd(cmd[0])
            if len(cmd_object_list) > 0:
                cmd_object_list[0].get_parser().print_help()
            else:
                raise CmdException, "cmd not found"
        else:
            raise CmdException, "too many cmd arguments"

################################################################################

class TCommandScript(Command):

    def add_args(self):
        self.get_parser().add_argument('scriptfile', action = "store", help='the script file name')

    def perform(self, argv):
        global _cmd_num
        ns = self.get_parser().parse_args(argv[1:])
        filename = ns.scriptfile
        if filename.endswith(".jc"):
            with open(ns.scriptfile) as fobj:
                lines = fobj.readlines()
                for i in range(len(lines)):
                    _cmd_num = i + 1
                    cmd = lines[i]
                    debug("[Line: %04d] %s" %(i + 1, cmd))
                    process_cmd(cmd)
        elif filename.endswith(".py"):
            execfile(filename, globals())
        else:
            pass

class TCommandLogLevel(Command):

    def add_args(self):
        self.get_parser().add_argument('log_level', action = "store", type = int, choices = (1, 2, 3, 4, 5, 6), help='the log level')

    def perform(self, argv):
        ns = self.get_parser().parse_args(argv[1:])
        set_log_level(ns.log_level)

class CommandCd(Command):

    def add_args(self):
        self.get_parser().add_argument('dirpath', help='the work directory to change')

    def perform(self, argv):
        ns = self.get_parser().parse_args(argv[1:])
        dirpath = ns.dirpath
        if os.path.isdir(dirpath):
            os.chdir(dirpath)
            debug(os.path.abspath(dirpath))
        else:
            error("dirpath invalid")

class CommandPwd(Command):

    def add_args(self):
        pass

    def perform(self, argv):
        dirpath = os.path.curdir
        debug(os.path.abspath(dirpath))

class CommandLL(Command):

    def add_args(self):
        pass

    def perform(self, argv):
        dir_list = os.listdir('.')
        for i in range(len(dir_list)):
            debug("%02d: %s" %(i, dir_list[i]))

class CommandW(Command):

    def add_args(self):
        self.get_parser().add_argument('logfile', help='the log file')

    def perform(self, argv):
        ns = self.get_parser().parse_args(argv[1:])
        logfile = ns.logfile
        if logfile == '-':
            set_log_file(sys.stdout)
        else:
            set_log_file(open(logfile, 'w+b'))

class TCommandSetVar(Command):

    def add_args(self):
        self.get_parser().add_argument('var', help='var name')
        self.get_parser().add_argument('value', help='var value')
        self.get_parser().add_argument('type', nargs = '?', default = 'str', choices = ('int', 'str'), help='var type')

    def perform(self, argv):
        ns = self.get_parser().parse_args(argv[1:])
        value = int(ns.value) if ns.type == 'int' else unicode(ns.value)
        _var_dict[ns.var] = value

class TCommandListVars(Command):

    def add_args(self):
        pass

    def perform(self, argv):
        keys = _var_dict.keys()
        keys.sort()
        for i in range(len(keys)):
            key = keys[i]
            value = _var_dict[key]
            if isinstance(value, (int, long)):
                vinfo = "0x%08X %d" %(value, value)
            else:
                vinfo = str(value)
            if key != '__builtins__':
                if not isinstance(value, (str, unicode)):
                    typeinfo = "[%s]" %type(value)
                else:
                    typeinfo = ""
                try:
                    debug("%02d : %s => %s %s" %(i, key.rjust(16), vinfo, typeinfo))
                except Exception:
                    debug("%02d : %s => %s %s" %(i, key.rjust(16), "", typeinfo))

class TCommandEcho(Command):

    def add_args(self):
        self.get_parser().add_argument('var', nargs = '*', help='the var name')

    def perform(self, argv):
        ns = self.get_parser().parse_args(argv[1:])
        debug(' '.join(ns.var))

class TCommandDump(Command):

    def add_args(self):
        self.get_parser().add_argument('var', nargs = '*', help='the var name')

    def perform(self, argv):
        ns = self.get_parser().parse_args(argv[1:])
        debug(ds(b(''.join(ns.var)), True, True))

class CommandVersion(Command):

    def add_args(self):
        pass

    def perform(self, argv):
        info(__version__)
        info(__copyright__)

_python_in_flag = False
_python_cmd_list = []

class CommandPythonBegin(Command):

    def add_args(self):
        pass

    def perform(self, argv):
        debug("python begin")
        global _python_in_flag
        _python_in_flag = True

def exec_python():
    global _python_cmd_list
    _python_cmd_list.insert(0, '#' * 80)
    _python_cmd_list.insert(0, '')
    _python_cmd_list.append('#' * 80)
    _python_cmd_list.append('')
    cmd = '\n'.join(_python_cmd_list)
    _python_cmd_list = []
    debug(cmd)
    c = compile(cmd, 'python command error', mode='exec')
    exec c in _var_dict

class CommandPythonEnd(Command):

    def add_args(self):
        pass

    def perform(self, argv):
        debug("python end")
        global _python_in_flag
        _python_in_flag = False
        exec_python()

################################################################################

_var_pattern = re.compile(r"\$?[{']\s*(\w+)\s*[}']")
def filter_cmd_var(v):
    '''把变量替换成原始字符串'''
    value_list = []
    it = _var_pattern.finditer(v)
    pos = 0
    for m in it:
        var = m.groups()[0]
        start = m.start()
        end = m.end()
        if var in _var_dict:
            value = unicode(_var_dict[var])
            value_list.append(v[pos:start])
            value_list.append(value)
            pos = end
        else:
            raise CmdException, "var not found"
    value_list.append(v[pos:])
    v = ''.join(value_list)
    return v

################################################################################

def parse_cmd_string(cmd):
    '''处理双引号语义'''
    cells = []
    cell = []
    flag = False
    for c in cmd:
        if flag:
            if c == '"':
                flag = False
                continue
            else:
                cell.append(c)
        else:
            if c == '"':
                flag = True
                continue
            elif c == ' ':
                cells.append(''.join(cell))
                cell = []
            else:
                cell.append(c)
    cells.append(''.join(cell))
    cells = filter(lambda cell: len(cell) != 0, cells)
    print cells
    return cells

################################################################################

_cmd_cells = []

def process_cmd(cmd):
    '''处理一条命令'''
    global _cmd_num
    global _cmd_cells
    _cmd_num += 1
    cmd = decode(cmd)
    #python mode
    global _python_in_flag
    if _python_in_flag:
        if cmd.strip() == 'py-end':
            _python_in_flag = False
            exec_python()
        else:
            _python_cmd_list.append(cmd)
        return
    cmd = cmd.strip()
    if len(cmd) == 0:
        return
    #`//` are comments
    if cmd.startswith("//") or cmd.startswith("#"):
        return
    #`:`use for exec python command
    if cmd.startswith(":"):
        py_cmd = cmd[1:].strip()
        c = compile(py_cmd, 'python command error', mode='exec')
        exec c in _var_dict
        return
    #`'` used for output python var
    elif cmd.startswith("'"):
        var = cmd[1:].strip()
        if len(var) == 0:
            return
        if var in _var_dict:
            v = _var_dict[var]
            if isinstance(v, (int, long)):
                info = "0x%08X %d" %(v, v)
            else:
                info = str(v)
            debug(info)
        else:
            raise CmdException, "var not found"
        return
    #`!` used for shell cmd line
    elif cmd.startswith("!"):
        shell_cmd = cmd[1:].strip()
        if len(shell_cmd) == 0:
            return
        os.system(shell_cmd)
    else:
        #处理多行的情况
        if cmd.endswith('\\'):
            _cmd_cells.append(cmd[:-1])
            log.debug("wait more...")
            return
        else:
            _cmd_cells.append(cmd)
            cmd = ' '.join(_cmd_cells)
            _cmd_cells = []
            #log.debug(cmd)

        #jcshell command
        cmd = filter_cmd_var(cmd)
        #print cmd
        cmd_argv = parse_cmd_string(cmd)
        #print cmd_argv
        cmd_name = cmd_argv[0]
        cmd_object_list = find_cmd(cmd_name)
        if len(cmd_object_list) == 0:
            raise CmdException, "invalid command"
        elif len(cmd_object_list) == 1:
            return cmd_object_list[0].perform(cmd_argv)
        else:
            names = map(lambda obj: obj.get_name(), cmd_object_list)
            output_set(names, 30, 0x02)

_cmd_num = 0
_python_in_flag = False
_python_cmd_list = []

def process():
    set_log_level(5)
    global _python_in_flag
    while True:
        try:
            head_info = _plugin_name
            try:
                cmd = raw_input("%s> " %(head_info))
            except EOFError:
                _python_in_flag = False
                exec_python()
                continue
            process_cmd(cmd)
        #except AttributeError as e:
        #    error("env not ready")
        except IOError as e:
            error(str(e))
        except CmdExitException as e:
            pass
        except Exception as e:
            import traceback
            if get_log_level() >= 5:
                error(traceback.format_exc())
            error(str(e))

def main():
    global _cmd_dict
    register_plugins()
    init_readline()
    _cmd_dict = init_plugin_object(_plugin_dict[DEFAULT_PLUGIN_NAME])
    process_cmd("/app redis")
    process_cmd("redis-connect")
    process()

################################################################################

_scshell_cmd_dict = {
    "help"                  : CommandHelp,
    "?"                     : CommandHelp,
    "cd"                    : CommandCd,
    "pwd"                   : CommandPwd,
    "ll"                    : CommandLL,
    ">"                     : CommandW,

    "/app"                  : CommandApp,
    "/script"               : TCommandScript,
    "/log-level"            : TCommandLogLevel,

    "/set-var"              : TCommandSetVar,
    "/list-vars"            : TCommandListVars,
    "lv"                    : TCommandListVars,
    "/print"                : TCommandEcho,
    "/echo"                 : TCommandEcho,
    "/dump"                 : TCommandDump,
    "version"               : CommandVersion,

    "py-begin"              : CommandPythonBegin,
    "py-end"                : CommandPythonEnd,
}


_ivar_dict = {
    "pcmd"              : process_cmd,
    "b"                 : b,
    "s"                 : s,
}

class RedisClientPlugin(Plugin):
    def __init__(self):
        self.__name = DEFAULT_PLUGIN_NAME
        self.__cmd_dict = _scshell_cmd_dict
        self.__var_dict = _ivar_dict

    def get_name(self):
        return self.__name

    def get_cmd_dict(self):
        return self.__cmd_dict

    def get_var_dict(self):
        return self.__var_dict

    def get_ext_matches(self):
        return []

def register(plugin_dict):
    plugin_object = RedisClientPlugin()
    plugin_dict[plugin_object.get_name()] = plugin_object

################################################################################

if __name__ == '__main__':
    main()

