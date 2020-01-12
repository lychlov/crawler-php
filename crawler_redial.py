# -*- coding: utf-8 -*-
'''
Created on 2012-5-18

@author: Shen Min
'''

import time, os, urllib, urllib2, cookielib, base64,re,random
import crawler_utils

class mega_crawler_dial:
    def __init__(self, options):
        self.options = options
    
    def redial(self):
        ip_changed = False
        old_ip = self.get_current_ip()
        new_ip = None

        error_count = 2
        while error_count > 0:
            error = self.disconnect()
            if error:
                error_count -= 1
                time.sleep(2)
            else:
                error_count = -1
        time.sleep(10)

        error_count = 2
        while error_count > 0:
            error = self.connect()
            if not error:
                time.sleep(3)
                error_count = -1
                new_ip = self.get_current_ip()
            else:
                error_count -= 1
                time.sleep(10)
        if not (new_ip is None) and (new_ip <> old_ip):
            ip_changed = True
        else:
            ip_changed = False
            
        return ip_changed

    def disconnect(self):
        pass
    
    def connect(self):
        pass
    
    def get_current_ip(self):
        return crawler_utils.get_my_ipaddr()
    
class mega_crawler_dial_win_pppoe(mega_crawler_dial):
    def disconnect(self):
        r = os.system('rasdial %s /DISCONNECT' % self.options['DialPPPoEEntry'])
        if (r <> 0):
            return True
        else:
            return False
    
    def connect(self):
        r = os.system('rasdial %s %s %s' % (self.options['DialPPPoEEntry'], self.options['DialUsername'], self.options['DialPassword']))
        if (r <> 0):
            return True
        else:
            return False
                
class mega_crawler_dial_general_router(mega_crawler_dial):
    def disconnect(self):
        error = False
        if self.options['DialDisConnUrl'] <> '':
            try:
                opener = urllib2.build_opener()
                if (self.options['DialUsername'] <> ''):
                    headers = [('Authorization', 'Basic %s' % base64.encodestring('%s:%s' % (self.options['DialUsername'], self.options['DialPassword']))[:-1])]
                else:
                    headers = []
                if self.options['DialDisConnHeader'] <> {}:
                    for header_item in self.options['DialDisConnHeader']:
                        headers.append((header_item, self.options['DialDisConnHeader'][header_item]))
                opener.addheaders = headers
                if self.options['DialDisConnData'] == {}:
                    params = None
                else:
                    params = urllib.urlencode(self.options['DialDisConnData'])
                f = opener.open(fullurl = self.options['DialDisConnUrl'], data=params, timeout = 30)
                if (f.getcode() <> 200) and (f.getcode() <> 302):
                    print '* REDIAL ERR(disconn): router return code: %d' % f.getcode()
                    error = True
                else:
                    error = False
            except Exception as e:
                print '* REDIAL ERR(disconn): router exception : %s *' % e
                error = True
        return error
    
    def connect(self):
        error = False
        if self.options['DialConnUrl'] <> '':
            try:
                opener = urllib2.build_opener()
                if (self.options['DialUsername'] <> ''):
                    headers = [('Authorization', 'Basic %s' % base64.encodestring('%s:%s' % (self.options['DialUsername'], self.options['DialPassword']))[:-1])]
                else:
                    headers = []
                if self.options['DialConnHeader'] <> {}:
                    for header_item in self.options['DialConnHeader']:
                        headers.append((header_item, self.options['DialConnHeader'][header_item]))
                opener.addheaders = headers
                if self.options['DialConnData'] == {}:
                    params = None
                else:
                    params = urllib.urlencode(self.options['DialConnData'])
                f = opener.open(fullurl = self.options['DialConnUrl'], data=params, timeout = 30)
                if (f.getcode() <> 200) and (f.getcode() <> 302):
                    print '* REDIAL ERR(conn): router return code: %d' % f.getcode()
                    error = True
                else:
                    error = False
            except Exception as e:
                print '* REDIAL ERR(conn): router exception : %s *' % e
                error = True

        return error

class mega_crawler_dial_f460(mega_crawler_dial):
    def disconnect(self):
        error = False
        if self.options['DialConnUrl'] <> '':
            try:
                opener = urllib2.build_opener()
                f = opener.open(fullurl = self.options['DialDisConnUrl'], timeout = 30)
                content = f.read()
                m = re.search('"Frm_Logintoken"\)\.value = "(\d+)"', content)
                params = {'Username':'useradmin', 'Password':'mwvvt', 'Frm_Logintoken':m.group(1)}
                params = urllib.urlencode(params)
                f = opener.open(fullurl = self.options['DialDisConnUrl'], data=params, timeout = 30)
                f = opener.open(fullurl = self.options['DialConnUrl'], timeout = 30)
                if (f.getcode() <> 200) and (f.getcode() <> 302):
                    print '* REDIAL ERR(conn): router return code: %d' % f.getcode()
                    error = True
                else:
                    #sleep 120 when success. this router is slow
                    time.sleep(120)
                    error = False
            except Exception as e:
                print '* REDIAL ERR(conn): router exception : %s *' % e
                error = True
        return error
    
    def connect(self):
        error = False
        return error

class mega_crawler_dial_HG220G(mega_crawler_dial):
    def disconnect(self):
        error = False
        if self.options['DialConnUrl'] <> '':
            try:
                cj = cookielib.CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                f = opener.open(fullurl = self.options['DialDisConnUrl'], timeout = 30)
                params = {'username':self.options['DialUsername'], 'password':self.options['DialPassword']}
                params = urllib.urlencode(params)
                f = opener.open(fullurl = self.options['DialDisConnUrl'], data=params, timeout = 30)
                f = opener.open(fullurl = self.options['DialConnUrl'], timeout = 30)
                content = f.read()
                m = re.search('sessionKey=\'(\d+)\'', content)
                if m:
                    f = opener.open(fullurl = 'http://192.168.1.1/rebootinfo.cgi?sessionKey=%s' % m.group(1) , timeout = 30)
                    #sleep 120 when success. this router is slow
                    time.sleep(120)
                else:
                    error = True
            except Exception as e:
                print '* REDIAL ERR(conn): router exception : %s *' % e
                error = True
        return error
    
    def connect(self):
        error = False
        return error

class mega_crawler_dial_e8c(mega_crawler_dial):
    def disconnect(self):
        error = False
        if self.options['DialConnUrl'] <> '':
            try:
                opener = urllib2.build_opener()
                f = opener.open(fullurl = 'http://192.168.1.1/login.html', timeout = 30)
                f = opener.open(fullurl = 'http://192.168.1.1/checkuser.cgi?checkusername=useradmin&checkpassword=ej2jy', timeout = 30)
                f = opener.open(fullurl = 'http://192.168.1.1/setcookie.cgi?setcookiekey=639936219', timeout = 30)
                str = 'Authorization=Basic %s' % base64.standard_b64encode('%s/%s/%s:%s' % (random.randrange(1, 1000), '639936219', 'useradmin', 'ej2jy'))
                opener = urllib2.build_opener()
                opener.addheaders=[('Cookie', str),]
                f = opener.open(fullurl = 'http://192.168.1.1/index.html', timeout = 30)
                f = opener.open(fullurl = 'http://192.168.1.1/resetrouter.html', timeout = 30)
                content = f.read()
                m = re.search('sessionKey=(\d+)\'', content)
                if m:
                    f = opener.open(fullurl = 'http://192.168.1.1/rebootinfo.cgi?sessionKey=%s' % m.group(1) , timeout = 30)
            except Exception as e:
                print '* REDIAL ERR(conn): router exception : %s *' % e
                error = True
        return error
    def connect(self):
        error = False
        return error
        
def get_dialer(options):
    if options['DialType'] == 'Win-PPPoE':
        d = mega_crawler_dial_win_pppoe(options)
    elif options['DialType'] == 'General-Router':
        d = mega_crawler_dial_general_router(options)
    elif options['DialType'] == 'F460':
		d = mega_crawler_dial_f460(options)
    elif options['DialType'] == 'HG220G':
        d = mega_crawler_dial_HG220G(options)
    elif options['DialType'] == 'e8-C':
    	d = mega_crawler_dial_e8c(options)
    else:
        d = None
    return d

def redial(options):
    d = get_dialer(options)
    if not d is None:
        return d.redial()
    else:
        return False

def __test():
    import crawler_options
    print 'start to test redial...'
    options = crawler_options.get_options()
    if redial(options) == True:
        print 'finished testing redial...OK'
    else:
        print 'finished testing redial...failed!'
    
if __name__ == '__main__':
    __test()