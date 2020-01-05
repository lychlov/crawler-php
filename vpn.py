#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2015-05-02

@author: Pani
'''

import sys, time, os, random, urllib2 ,ConfigParser
import crawler_utils

#def main(args):
#    while True:
#        if not os.path.isfile(crawler_utils.get_run_dir() + '/netlink'):
#            changeip()
#            continue
#        stime = random.randint(180,600)    
#        if (time.time()-(os.stat(crawler_utils.get_run_dir() + '/netlink').st_mtime))>stime:
#            changeip()
#            continue
#        if not os.path.isfile(crawler_utils.get_run_dir() + '/net.lock'): 
#            try:
#                content = urllib2.urlopen('http://www.ip.cn/').read() 
#                if "上海" in content:
#                    print 'IP is SH'
#                    changeip()
#                    time.sleep(10)
#            except Exception as e:
#                print 'ERR: %s' % e
ERROR_BLOCK = False
#VPN_NAME = 'abc'
#VPN_USERNAME = '018'
#VPA_PASE = '123456'
def changeip():
    try:
    	'''
        iplist = []
        i = 0;
        fp = open ('vpn_ip_list.txt', 'r')
        for ip in fp:
            ip = ip.strip();
            if ip == "":
                continue;
            iplist.append(ip)
        fp.close()
        key = random.randint(0,len(iplist)-1)
        useip = iplist[key]
        
        useip = 'p.sr16.com'
        print 'ip:' + useip
        '''
        change_vpn_st = time.time()
        disconnect()
        
        '''
        fw = open (r'C:\Windows\System32\ras\rasphone.pbk', 'w')
        fw.write("[VPN_C]\n")
        fw.write("MEDIA=rastapi\n")
        fw.write("Port=VPN1-0\n")
        #fw.write("Device=WAN Miniport (IKEv2)\n")
        fw.write("DEVICE=vpn\n")
        fw.write("PhoneNumber=%s\n" %(useip))
        fw.close()
        '''
        connect()
        if (time.time() - change_vpn_st) <= 0:
        	print "Client OS restart"
        	r = os.system('shutdown -r -t 0')
        
    except Exception as e:
        print 'ERR: %s' % e
        #log.log_msg('ERR: %s' % e)
    
    #finally:
        #print 'crawler(crawler id: %s) terminated' % crawler_id
        #log.log_msg('crawler(crawler id: %s) terminated' % crawler_id)


def disconnect():

        #h = open(crawler_utils.get_run_dir() + '/net.lock', 'w')
        #h.write('change ip')
        #h.close()
        #h = open(crawler_utils.get_run_dir() + '/netlink', 'w')
        #h.write('change ip')
        #h.close()
        # if(isinstance(VPN_NAME, str)):
        #    linkname = VPN_NAME.encode('gb2312')
        # else:
        #    linkname = VPN_NAME.decode('utf8').encode('gb2312')
        if os.path.exists('adsl.ini'):
            config = ConfigParser.ConfigParser()
            config.readfp(open('adsl.ini'))
            if config.get("VPN_SETTING","adsl_name") <> "":
                vpn_name = config.get("VPN_SETTING","adsl_name")
            if config.get("VPN_SETTING","adsl_username") <> "":
                vpn_username = config.get("VPN_SETTING","adsl_username")
            if config.get("VPN_SETTING","adsl_pass") <> "":
                passwd = config.get("VPN_SETTING","adsl_pass")
        vpn_name = vpn_name.strip()
        vpn_username = vpn_username.strip()
        passwd = passwd.strip()
        r = os.system('rasdial '+vpn_name+' /DISCONNECT')
        if (r <> 0):
            return True
        else:
            return False
    
def connect():
        try:
        	#route add 122.144.130.111 mask 255.255.255.255 192.168.1.1
        	#ADSL账号：SR9413953 密码：522584
            if os.path.exists('adsl.ini'):
                config = ConfigParser.ConfigParser()
                config.readfp(open('adsl.ini'))
                if config.get("VPN_SETTING","adsl_name") <> "":
                    vpn_name = config.get("VPN_SETTING","adsl_name")
                if config.get("VPN_SETTING","adsl_username") <> "":
                    vpn_username = config.get("VPN_SETTING","adsl_username")
                if config.get("VPN_SETTING","adsl_pass") <> "":
                    passwd = config.get("VPN_SETTING","adsl_pass")
            vpn_name = vpn_name.strip()
            vpn_username = vpn_username.strip()
            passwd = passwd.strip()
            r = os.system('rasdial %s %s %s' % (vpn_name, vpn_username, passwd))
            #print VPN_NAME, VPN_USERNAME, VPA_PASE
            #exit()
            #r = os.system('rasdial %s %s %s' % ('VPN_C', 'SR1549297', '210169'))
            if r != 0:
                changeip()

            #if not check_lo():
            #    changeip()
            
            return True
        except Exception as e:
            print 'Connect ERR: %s' % e
            changeip()
            return False
        #os.remove(crawler_utils.get_run_dir() + '/net.lock')    

def check_lo():
    content = urllib2.urlopen('http://1111.ip138.com/ic.asp').read()
    if '101.81.79.195' in content:
       print "vpn change failed"
       return False
    
    return True
    
    
    
#if __name__ == '__main__':
#    main(sys.argv)
