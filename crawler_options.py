# -*- coding: utf-8 -*-
'''
Created on 2012-5-18

@author: Shen Min
'''

import xml.parsers.expat
import crawler_utils

reading_dial_type = False
reading_dial_conn_url = False
reading_dial_disconn_url = False
reading_dial_username = False
reading_dial_password = False
reading_dial_pppoe_entry = False

options = {
    'DialType':'',
    'DialConnUrl':'',
    'DialDisConnUrl':'',
    'DialUsername':'',
    'DialPassword':'',
    'DialPPPoEEntry':'',
    'DialConnData':'',
    'DialDisConnData':'',
    'DialConnHeader':'',
    'DialDisConnHeader':''
}

def __start_element(name, attrs):
    global reading_dial_type, reading_dial_conn_url, reading_dial_disconn_url, reading_dial_username, reading_dial_password, reading_dial_pppoe_entry
    if name == 'DialType':
        reading_dial_type = True
    elif name == 'DialConnUrl':
        reading_dial_conn_url = True
    elif name == 'DialDisConnUrl':
        reading_dial_disconn_url = True
    elif name == 'DialUsername':
        reading_dial_username = True
    elif name == 'DialPassword':
        reading_dial_password = True
    elif name == 'DialPPPoEEntry':
        reading_dial_pppoe_entry = True
    elif name == 'DialConnData':
        options['DialConnData'] = attrs
    elif name == 'DialDisConnData':
        options['DialDisConnData'] = attrs
    elif name == 'DialConnHeader':
        options['DialConnHeader'] = attrs
    elif name == 'DialDisConnHeader':
        options['DialDisConnHeader'] = attrs
        
def __end_element(name):
    global reading_dial_type, reading_dial_conn_url, reading_dial_disconn_url, reading_dial_username, reading_dial_password, reading_dial_pppoe_entry
    if name == 'DialType':
        reading_dial_type = False
    elif name == 'DialConnUrl':
        reading_dial_conn_url = False
    elif name == 'DialDisConnUrl':
        reading_dial_disconn_url = False
    elif name == 'DialUsername':
        reading_dial_username = False
    elif name == 'DialPassword':
        reading_dial_password = False
    elif name == 'DialPPPoEEntry':
        reading_dial_pppoe_entry = False
        
def __char_data(data):
    global reading_dial_type, reading_dial_conn_url, reading_dial_disconn_url, reading_dial_username, reading_dial_password, reading_dial_pppoe_entry
    global options
    if reading_dial_type:
        options['DialType'] = str(data)
    elif reading_dial_conn_url:
        options['DialConnUrl'] = str(data)
    elif reading_dial_disconn_url:
        options['DialDisConnUrl'] = str(data)
    elif reading_dial_username:
        options['DialUsername'] = str(data)
    elif reading_dial_password:
        options['DialPassword'] = str(data)
    elif reading_dial_pppoe_entry:
        options['DialPPPoEEntry'] = str(data)

def get_options(optionfile = crawler_utils.get_run_dir() + '/settings.xml'):
    x = xml.parsers.expat.ParserCreate()
    x.StartElementHandler = __start_element
    x.EndElementHandler = __end_element
    x.CharacterDataHandler = __char_data

    try:
        global options
        x.ParseFile(open(optionfile, 'r'))
    except:
        pass

    return options