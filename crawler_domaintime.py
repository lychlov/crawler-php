#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2015-7-2

@author: Galen
'''

import sys, os, time, datetime
import crawler_utils

def get_time(domain):
    if os.path.isfile(crawler_utils.get_run_dir() + '/net.lock'):
        return 2
    con = 'run'
    domaindir = crawler_utils.get_run_dir() + '/domain/'
    domainfile = domain.replace('.','')
    domainfile = domainfile.replace('-','_')
    domainfile = domaindir + domainfile
    if not os.path.exists(domaindir):
        os.makedirs(domaindir)

    if not os.path.isfile(domainfile):
        h = open(domainfile, 'w')
        h.write(con)
        h.close()
        
    now = str(time.time())
    fctime = time.ctime(os.stat(domaindir).st_mtime)
    if (time.time()-(os.stat(domainfile).st_mtime))>2:
        h = open(domainfile, 'w')
        h.write(con)
        h.close()
        return 0
    return 1
