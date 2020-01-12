# -*- coding: utf-8 -*-
'''
Created on 2012-5-17

@author: Shen Min
'''

import urllib2, time
import crawler_consts,vpn

def svr_get_tasks(crawler_id, log, domain):
    error = True
    data = None
    rtry = 0
    while error:
        try:
            url = 'http://54.221.121.173/api.php?k=123456&method=GetTask&client_id=%s' % (crawler_id)
            opener = urllib2.build_opener()
            f = opener.open(fullurl = url, timeout = 120)
            if f.getcode() <> 200:
                error = True
            else:
                error = False
        except Exception as inst:
            err_str = '%s' % inst
            print '** ERR: svr_get_tasks (%s)' % err_str
            log.log_msg('** ERR: svr_get_tasks (%s)' % err_str)
            error = True
        if not error:
            data = f.read()
        else:
            time.sleep(30)
            rtry += 1
            if rtry > 5:
            	vpn.changeip()
            	rtry = 0
    return data

def srv_put_tasks_result(crawler_id, tasks, params, log):
    error = True
    data = None
    err_count = 0
    # print params
    # exit()
    while error:
        try:
            url = 'http://54.221.121.173/api.php?k=123456&method=SetTask&client_id=%s' % (crawler_id)
            opener = urllib2.build_opener()
            f = opener.open(fullurl = url, data=params, timeout = 300)
            if f.getcode() <> 200:
                error = True
            else:
                error = False
        except Exception as inst:
            
            err_str = '%s' % inst
            print '** ERR: svr_put_tasks_result (%s)' % err_str
            # log.log_msg('** ERR: svr_put_tasks_result (%s)' % err_str)
            error = True
            err_count += 1
        if not error:
            data = f.read()
        else:
            if err_count > 3:
                return None
            else:
                time.sleep(5)
    return data

