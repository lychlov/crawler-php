#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2012-5-17

@author: Li Wei
'''

import sys, uuid, os
import crawler_utils
from urllib import quote

def get_id():
    id = '%s' % uuid.uuid4()
    h = None
    try:
        h = open(crawler_utils.get_run_dir() + '/uuid.txt', 'r')
        h.seek(0)
        id = h.readline()
        if len(id) < 1:
            id = '%s' % uuid.uuid4()
    except:
        pass
    finally:
        if h:
            h.close()
    if not os.path.isfile(crawler_utils.get_run_dir() + '/uuid.txt'):
        try:
            h = open(crawler_utils.get_run_dir() + '/uuid.txt', 'w')
            h.write(id)
        except:
            pass
        finally:
            if h:
                h.close()
    return quote(id)

