# -*- coding: utf-8 -*-
'''
Created on 2012-5-17

@author: Shen Min
'''

import crawler_svr, crawler_helper, urllib, time
import json

def get_tasks(crawler_id, log, domain):
    while True:
        task_data = crawler_svr.svr_get_tasks(crawler_id, log, domain)
        if not (task_data is None):
            try:
                task_json = json.loads(task_data)
                # print task_json['results']
                # exit()
                if task_json['resultcode'] == 200:
                    return task_json['results']
            except Exception,e:
                # print e
                print '** ERR: get_tasks (json decode)'
                log.log_msg( '** ERR: get_tasks (json decode)')
                time.sleep(10)
            
def proc_tasks(crawler_id, tasks, options, log, proxy):
    tasks_proc_obj = crawler_helper.mega_crawler_task_proc(crawler_id, tasks, options, log, proxy)
    # if tasks['task_type'] == 'get_page_content':
    #     tasks_proc_obj = crawler_helper.mega_crawler_task_proc(crawler_id, tasks, options, log, proxy)
    # else:
    #     tasks_proc_obj = None
        
    if tasks_proc_obj is None:
        r = None
    else:
        r = tasks_proc_obj.proc_task()
    return r

def put_tasks_result(crawler_id, tasks, result, options, log):
    p = {}
    # print result
    # exit()
    for i, r in enumerate(result):
        key_name = 'url%d' % (i + 1)
        p[key_name] = r['download_result']['url']
        p['%s_id' % key_name] = r['download_result']['urlid']
        p['%s_code' % key_name] = r['download_result']['code']
        p['%s_header' % key_name] = r['download_result']['header']
        p['%s_content' % key_name] = r['download_result']['content']
        
    p['urlcount'] = len(result)
    # print p
    # exit()
    # params = p
    try:
        params = urllib.urlencode(p)
    except:
        print '** ERR: put_tasks_result (url encode)'
        return None
    
    # print params
    # exit()

    while True:
        got_data = crawler_svr.srv_put_tasks_result(crawler_id, tasks, params, log)
        time.sleep(5)
        print got_data
        return 1
        file_object = open('thefile.txt', 'a')
        file_object.write(got_data)
        file_object.close()
        if not (got_data is None):
            try:
                data_json = json.loads(got_data)
                if data_json['resultcode'] <> 200:
                    print '** ERR: put_tasks_result (got incorrect result code (%d) when submitting tasks)' % data_json['resultcode']
                    # log.log_msg('** ERR: put_tasks_result (got incorrect result code (%d) when submitting tasks)' % data_json['resultcode'])
                return data_json['results']
            except:
                print '** ERR: put_tasks_result (json decode)'
                # log.log_msg( '** ERR: put_tasks_result (json decode)')                
                time.sleep(10)
        else:
            return None
                
                