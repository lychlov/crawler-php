# -*- coding: utf-8 -*-
'''
Created on 2012-5-17

@author: Li Wei
'''

import time, json, random
import crawler_svr

class Proxy:
    def __init__(self, crawler_id, log):
        self.timestamp = None
        self.proxies = None
        self.crawler_id = crawler_id
        self.log = log

    def get(self):
        current = time.time()
        if self.proxies == None or self.timestamp == None or current - self.timestamp >= 3600 or len(self.proxies) == 0:
            print 'refresh proxy...'
            proxy_string = crawler_svr.svr_get_proxy(self.crawler_id, self.log)
            if not (proxy_string is None):
                try:
                    data = json.loads(proxy_string)
                    if data['resultcode'] == 200:
                        self.proxies = data['results']
                        self.timestamp = time.time()
                except:
                    print '** ERR: get_proxy (json decode)'
                    self.log.log_msg( '** ERR: get_proxy (json decode)')
        if self.proxies != None and current - self.timestamp < 3600 and len(self.proxies) > 0:
            return random.choice(self.proxies)
