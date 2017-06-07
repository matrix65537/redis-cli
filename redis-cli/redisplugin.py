#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from scplib import *
from iplugin import Plugin
from icommand import *
from state import *

from redisclient import RedisClient

_redis = RedisClient()

class CommandRedisConnect(Command):

    def add_args(self):
        self.get_parser().add_argument('-i', '--ip', dest = 'ip', metavar = 'ip', default = "127.0.0.1", help='the server ip')
        self.get_parser().add_argument('-p', '--port', metavar = 'port', action = "store", default = '6379', help='the server port')

    def perform(self, argv):
        ns = self.get_parser().parse_args(argv[1:])
        _redis.connect(ns.ip, int(ns.port))

class CommandSend(Command):

    def add_args(self):
        self.get_parser().add_argument('cmd', nargs = '+')

    def perform(self, argv):
        ns = self.get_parser().parse_args(argv)
        rsp = _redis.transmit(ns.cmd)
        log.debug(rsp)

class CommandCrsLs(Command):

    def add_args(self):
        self.get_parser().add_argument('-a', '--aid', dest = 'aid', metavar = 'aid', default = "", help='the aid')
        self.get_parser().add_argument('-s', '--search-criteria', dest = 'search_criteria', metavar = 'search_criteria', default = "", help='the search criteria')

    def perform(self, argv):
        ns = self.get_parser().parse_args(argv[1:])
        crsapp = CRS(get_com_obj())
        crsapp.select()
        aid = b(ns.aid)
        tlv4F = TLV("4F", aid, TLV.TYPE_BYTES)
        cmddata = tlv4F.to_bytes() + b(ns.search_criteria)
        return crsapp.get_status(cmddata)

class CommandCrsActive(Command):

    def add_args(self):
        self.get_parser().add_argument('instance_aid', metavar = 'AID', help='the instance aid')

    def perform(self, argv):
        ns = self.get_parser().parse_args(argv[1:])
        instance_aid = b(ns.instance_aid)
        crsapp = CRS(get_com_obj())
        crsapp.select()
        crsapp.set_status_availability_state_over_cl(P2_STATUS_VALUE_CONTACTLESS_ACTIVATION_ACTIVATED, [instance_aid])

class CommandCrsDeActive(Command):

    def add_args(self):
        self.get_parser().add_argument('instance_aid', metavar = 'AID', help='the instance aid')

    def perform(self, argv):
        ns = self.get_parser().parse_args(argv[1:])
        instance_aid = b(ns.instance_aid)
        crsapp = CRS(get_com_obj())
        crsapp.select()
        crsapp.set_status_availability_state_over_cl(P2_STATUS_VALUE_CONTACTLESS_ACTIVATION_DEACTIVATED, [instance_aid])

_redis_cmd_dict = {
    "redis-connect" : CommandRedisConnect,
    ".*"            : CommandSend,
}

class RedisPlugin(Plugin):
    def __init__(self):
        self.__name = "redis"
        self.__cmd_dict = _redis_cmd_dict
        self.__var_dict = {}

    def get_name(self):
        return self.__name

    def get_cmd_dict(self):
        return self.__cmd_dict

    def get_var_dict(self):
        return self.__var_dict

    def get_ext_matches(self):
        return []

def register(plugin_dict):
    plugin_object = RedisPlugin()
    plugin_dict[plugin_object.get_name()] = plugin_object

