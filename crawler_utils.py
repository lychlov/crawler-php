# -*- coding: utf-8 -*-
'''
Created on 2012-5-18

@author: Shen Min
'''

import sys, os, re, urllib2

def get_run_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)
    
def get_my_ipaddr():
    ipgetter = get_ipaddr()
    return ipgetter.getip()
    
class get_ipaddr:
    def getip(self):
        try:
            myip = self.visit("http://ipdetect.dnspark.com")
        except:
            try:
                myip = self.visit("http://whereismyip.com/")
            except:
                myip = None
        return myip
    
    def visit(self, url):
        opener = urllib2.urlopen(url)
        if url == opener.geturl():
            str = opener.read()
        return re.search('\d+\.\d+\.\d+\.\d+',str).group(0)
    