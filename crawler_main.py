#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2012-5-17

@author: Shen Min
'''

import sys, uuid, time, re, shutil, os, threading, random, socket
import crawler_uid, crawler_task, crawler_options, crawler_redial, crawler_consts, crawler_log, crawler_updater, crawler_utils, crawler_autorun, crawler_domaintime, vpn
from crawler_proxy import Proxy

def main(args):
    task_domain = None
    if (len(args) >= 2):
        task_domain = args[1]
    '''
    m = re.match('.*update\.tmp', crawler_utils.get_run_dir(), re.IGNORECASE)
    if m:
        print '** updating **'
        time.sleep(3)
        target_file = sys.executable.replace('update.tmp\\','')
        shutil.copy(sys.executable, target_file)
        os.popen('start "" "%s"' % target_file)
        return
    else:
        if os.path.exists(crawler_utils.get_run_dir() + '\\update.tmp\\'):
            print '** clearing **'
            time.sleep(3)
            try:
                shutil.rmtree(crawler_utils.get_run_dir() + '\\update.tmp\\')
            except:
                pass
	'''

    try:
        # init
        if os.name == 'nt' and not task_domain:
            crawler_autorun.win_autorun('mega_crawler', sys.executable)

        filelist = os.listdir(crawler_utils.get_run_dir())
        patharr = os.path.split(sys.executable)
        for line in filelist:
            n = re.match('.*\.exe$', line, re.IGNORECASE)
            if n and line <> patharr[1]:
                # shutil.rmtree(crawler_utils.get_run_dir()+"/"+line)
                os.remove(crawler_utils.get_run_dir()+"\\"+line)
        crawler_id = crawler_uid.get_id()
        options = crawler_options.get_options()
        log = crawler_log.mega_crawler_log(crawler_id)
        proxy = Proxy(crawler_id, log)
        # if os.path.exists('adsl.ini'):
        #     config = ConfigParser.ConfigParser()
        #     config.readfp(open('adsl.ini'))
        #     if config.get("VPN_SETTING","adsl_name") <> "":
        #         vpn.VPN_NAME = config.get("VPN_SETTING","adsl_name")
        #     if config.get("VPN_SETTING","adsl_username") <> "":
        #         vpn.VPN_USERNAME = config.get("VPN_SETTING","adsl_username")
        #     if config.get("VPN_SETTING","adsl_pass") <> "":
        #         vpn.PASS = config.get("VPN_SETTING","adsl_pass")
        # print vpn.VPN_NAME,vpn.VPN_USERNAME,vpn.PASS
        # exit()       
        print crawler_consts.MEGA_CRAWLER_VERSTRING + '\n' + '=' * 70
        print 'start (crawler id: %s)...' % crawler_id
        print '  @%s' % sys.executable
        log.log_msg('start (crawler id: %s)...' % crawler_id)
        socket.setdefaulttimeout(60)
        # main loop
        last_sleep_time = 10
        last_checkupdate_time = 0
        version_checkupdate_time = time.time()
        first_start = True
        c_threads = []
        pc = 0
        pi = 0
        main_thread = threading.currentThread()
        while True:

            #Redail VPN
            # if vpn.ERROR_BLOCK == True:
            #     print "403 block -> change vpn"
            #     for t in threading.enumerate():
            #         if t is main_thread:
            #             continue
            #         t.join()
                                
            #     #c_threads = []
            #     vpn.changeip()
            #     vpn.ERROR_BLOCK = False
            #     last_checkupdate_time = time.time()
            # elif time.time() - last_checkupdate_time >= 1800:
            #     print "change vpn"
            #     for t in threading.enumerate():
            #         if t is main_thread:
            #             continue
            #         t.join()
                
            #     #c_threads = []
                
            #     vpn.changeip()
            #     last_checkupdate_time = time.time()
            #     vpn.ERROR_BLOCK = False

            # check updates
            #last_checkupdate_time = 0
            #if time.time() - version_checkupdate_time >= 3600 or time.time() - version_checkupdate_time<20:
                #print 'check for an update'
                #log.log_msg('check for an update')
                #last_checkupdate_time = time.time()
                #if crawler_updater.check_and_update(crawler_id, log) == True:
                    #break    

            # get tasks
            tasks = crawler_task.get_tasks(crawler_id, log, task_domain)

            # print tasks
            # exit()
            # proc tasks
            no_task = tasks.get('NoTask', None)
            if no_task <> None:
                print 'no task got, [reason:%s]' % no_task
                log.log_msg('no task got, [reason:%s]' % no_task)
                time.sleep(20)
                r = None
            else: 
                # if vpn.ERROR_BLOCK == True:
                #     print "403 block -> change vpn right now !!"
                #     vpn.changeip()
                #     vpn.ERROR_BLOCK = False
                #     last_checkupdate_time = time.time()
                # else:    
                print "Total Threads: %d" %(len(threading.enumerate()))
                if len(threading.enumerate()) >= 5:
                    print 'waiting...# finished'
                    for t in threading.enumerate():
                        if t is main_thread:
                            continue
                        t.join()
                        break
                    
                    #c_threads = []
                process = task_thread(crawler_id, tasks, options, log, proxy)
                process.start()
                #c_threads.append(process)
                
                

            # wait for next round
            print 'wait for next getting tasks(sleep %d secs)' % last_sleep_time
            log.log_msg('wait for next getting tasks(sleep %d secs)' % last_sleep_time)
            
            time.sleep(last_sleep_time)
        
    except Exception as e:
        print 'ERR: %s' % e
        log.log_msg('ERR: %s' % e)
    
    finally:
        print 'crawler(crawler id: %s) terminated' % crawler_id
        log.log_msg('crawler(crawler id: %s) terminated' % crawler_id)

class task_thread(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, crawler_id, tasks, options, log, proxy):  
        threading.Thread.__init__(self)  
        self.crawler_id = crawler_id  
        self.tasks = tasks
        self.options = options
        self.log = log
        self.proxy = proxy
   
    def run(self): #Overwrite run() method, put what you want the thread do here  
        print 'got %d tasks' % (len(self.tasks['urls']))
        self.log.log_msg('got %d tasks' % (len(self.tasks['urls'])))
        # exit()
        try:
            r = crawler_task.proc_tasks(self.crawler_id, self.tasks, {}, {}, {})
        except Exception as e:
            print 'ERR: %s' % e
            # self.log.log_msg('ERR: %s' % e)
            return
            #continue
        # print 'start to submit results of task[id:%d]' % (self.tasks['task_id'])
        # self.log.log_msg('start to submit results of task[id:%d]' % (self.tasks['task_id']))

        # submit results
        # print r
        # exit()
        r = crawler_task.put_tasks_result(self.crawler_id, self.tasks, r, {}, {})
        if r is None:
            print 'failed to submit results'
            # self.log.log_msg('failed to submit results of task[id:%d], given up' % (tasks['task_id']))
        else:
            print 'finished to submit results'
            # self.log.log_msg('finished to submit results of task[id:%d]' % (self.tasks['task_id']))
            try:
                last_sleep_time = r['GetTaskAfter']
            except:
                last_sleep_time = 30
        
if __name__ == '__main__':
    main(sys.argv)
