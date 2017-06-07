#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

_comobj             = None
_scobj              = None
_var_dict           = None

def set_com_obj(comobj):
    global _comobj
    _comobj = comobj

def get_com_obj():
    return _comobj

def set_sc_obj(scobj):
    global _scobj
    _scobj = scobj

def get_sc_obj():
    return _scobj

def set_var_dict(var_dict):
    global _var_dict
    _var_dict = var_dict

def get_var_dict():
    return _var_dict

