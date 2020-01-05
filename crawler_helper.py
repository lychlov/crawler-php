# -*- coding: utf-8 -*-
'''
Created on 2012-5-18

@author: Shen Min
'''

import time, urllib2, urllib, re, vpn,random,zlib
import requests,retailmenot_helper
from crawler_proxy import Proxy
from urlparse import urlparse

class mega_crawler_task_proc:
    def __init__(self, crawler_id, tasks, options, log, proxy):
        self.crawler_id = crawler_id
        self.tasks = tasks
        self.options = options
        self.log = log
        self.blocked_domain = []
        self.proxy = proxy
    
    def proc_page(self, download_result): # for being inherited
        return None
    
    def download_page(self, url, header,urlid, postdata):
        retry = 2
        while True:
            retry = retry - 1
            if retry < 0:
                break
            try:
                # opener = urllib2.build_opener()
                # opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(random.randint(20,60)) + '.0.1847.116 Safari/537.36')]
                # opener.addheaders = [('User-agent', 'Googlebot/2.1 (+http://www.google.com/bot.html)')]
                #if self.tasks['task_rules']['useragent'] == '':
                #    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36')]
                #else:
                #    opener.addheaders = [('User-agent', self.tasks['task_rules']['useragent'])]  
                headersarr = ['Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1',
                'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                'Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; PRO 5 Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.2.942 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 5.1.1; OPPO A53 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043220 Safari/537.36 MicroMessenger/6.5.8.1060 NetType/4G',
                'Mozilla/5.0 (iPhone 6p; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.4.1 Mobile/14F89 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
                'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MI MAX Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/8.7.8',
                'Mozilla/5.0 (Linux; Android 7.0; MHA-AL00 Build/HUAWEIMHA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baiduboxapp/8.6.1 (Baidu; P1 7.0)',
                'Mozilla/5.0 (iPhone 6; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.4.1 Mobile/14F89 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
                'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; OPPO R9s Plus Build/MMB29M) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.7.6) WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21',
                'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM-G9280 Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.9.941 Mobile Safari/537.36',
                'Mozilla/5.0 (iPhone 92; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.4.1 Mobile/14F89 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
                'Mozilla/5.0 (Linux; Android 6.0.1; vivo X9Plus Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/4G WebP/0.3.0 Pixel/1080',
                'Mozilla/5.0 (Linux; Android 7.0; LON-AL00 Build/HUAWEILON-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/4G WebP/0.3.0 Pixel/1440',
                'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; R7Plusm Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.2.942 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 5.0.2; Redmi Note 2 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1920',
                'Mozilla/5.0 (Linux; Android 6.0; HUAWEI CRR-UL00 Build/HUAWEICRR-UL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043220 Safari/537.36 MicroMessenger/6.5.7.1041 NetType/4G Language/zh_CN',
                'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; ZUK Z1 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.4 Mobile Safari/537.36'
                ]
                i = random.randint(0,17)
                headers = {'User-Agent':headersarr[i],'Referer':url}

                # if header:
                #     headers = header.split("\n")
                #     for h in headers:
                #         p = h.split(':')
                #         if len(p) > 1:
                #             opener.addheaders.append((p[0], p[1]))

                posts = {}
                if postdata:
                    for p in postdata.split(","):
                        v = p.split('=')
                        if len(v) > 1:
                            posts[v[0]] = v[1]

                if len(posts) > 0:
                    # f = opener.open(fullurl = url, timeout = 15, data=urllib.urlencode(posts))
                    f = requests.post(url,headers=headers,data=urllib.urlencode(posts),timeout=60)
                else:
                    # f = opener.open(fullurl = url, timeout = 15)
                    f = requests.get(url,headers=headers,timeout=60)

            except Exception as inst:
                err_str = '%s' % inst
                if (err_str) == '<urlopen error timed out>':
                    result = {'code':408, 'header':'', 'content': '', 'url':url, 'newurl':'','urlid':urlid}
                    continue
                m = re.match('HTTP Error (\d+):', err_str, re.IGNORECASE)
                if (m and len(m.groups()) >= 1):
                    error_code = int(m.group(1))
                    result = {'code':error_code, 'header':'', 'content': '', 'url':url, 'newurl':'','urlid':urlid}
                    continue
                time.sleep(2)
            try:
                result = {'code':f.getcode(), 'header':f.headers, 'content': f.content, 'url':url, 'newurl':f.url,'urlid':urlid}
            except:
                result = {'code':0, 'header':'', 'content': '', 'url':url, 'newurl':'','urlid':urlid}
            #handle block page by news
            time.sleep(2)
            # print zlib.decompress(result['content'])
            if re.match(r".*?Please verify that", result['content']) or re.match(r".*?Please help us verify", result['content']):
                result['code'] = 403
            if result['code'] == 0:
                result['code'] = 403
            #end
            if result['code'] == 200:
                return result
			
            # if result['code'] != 200:
            #     result['code'] = 403

            # return result
        #try proxy
        #do not use proxy now
#        retry = 2
#        while True:
#            retry = retry - 1
#            if retry < 0:
#                break
#            try:
#                proxy = self.proxy.get()
#                if proxy is None or proxy['addr'] is None or proxy['port'] is None:
#                    if result is None:
#                        result = {'code':0, 'header':'', 'content': '', 'url':url, 'newurl':''}
#                    return result
#                hproxy = urllib2.ProxyHandler({"http" : '%s:%s' % (proxy['addr'], proxy['port'])})
#                opener = urllib2.build_opener(hproxy)
#                if self.tasks['task_rules']['useragent'] == '':
#                    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36')]
#                else:
#                    opener.addheaders = [('User-agent', self.tasks['task_rules']['useragent'])]
#                f = opener.open(fullurl = url, timeout = 20)
#            except Exception as inst:
#                err_str = '%s' % inst
#                if (err_str) == '<urlopen error timed out>':
#                    result = {'code':408, 'header':'', 'content': '', 'url':url, 'newurl':''}
#                    continue
#                m = re.match('HTTP Error (\d+):', err_str, re.IGNORECASE)
#                if (m and len(m.groups()) >= 1):
#                    error_code = int(m.group(1))
#                    result = {'code':error_code, 'header':'', 'content': '', 'url':url, 'newurl':''}
#                    continue
#                time.sleep(2)
#            try:
#                result = {'code':f.getcode(), 'header':f.headers, 'content': f.read(), 'url':url, 'newurl':f.geturl()}
#            except:
#                result = {'code':0, 'header':'', 'content': '', 'url':url, 'newurl':''}
#            if result['code'] == 200:
#                return result
        return result
    
    def download_bin(self, url):
        pass
    
    def proc_task(self): # for being called by caller
        result = []
        last_domain = ''
        # print self.tasks['urls']
        # exit()
        for i in self.tasks['urls']:

            url = self.tasks['urls'][i]['Url']
            urlid = self.tasks['urls'][i]['UrlId']
            if url is None:
                continue
            print '  processing: %s...' % (url)
            
            url_parse = urlparse(url)

            # print url
            # exit()
            # print url_parse
            # exit()
            domain = url_parse.netloc
#            if domain in self.blocked_domain:
#                continue
            parts = urlparse(url)
            host = parts.netloc
            
            no_content = False
            try:
                header = self.tasks['headers']['ahead'][i];
            except:
                header = '';

            try:
                postdata = self.tasks['headers']['post'][i];
            except:
                postdata = '';
            
            # #add by news
            # if vpn.ERROR_BLOCK == True :
            #     continue

            try:
                download_result = self.download_page(url, header,urlid, postdata)
            except Exception as inst:
                no_content = True
                if type(inst[0]) is int:
                    download_result = {'code':inst[0], 'header':'', 'content': '', 'url':url, 'newurl':url,'urlid':urlid}
                else:
                    download_result = {'code':0, 'header':'', 'content': '', 'url':url, 'newurl':url,'urlid':urlid}

            # print download_result
            # exit()
            
            if 'sorry but your usage of this site resembles automated software' in download_result['content']:
            	print "content block"
            	download_result['code'] = 403
            
            print download_result['code']

            #or download_result['code'] == 408:
            if download_result['code'] == 403:
                vpn.ERROR_BLOCK = True
            
            # self.log.log_msg('  processing(%d): %s ...%d' % (i + 1, url, download_result['code']))
            
            if (no_content == False):
                page_result = self.proc_page(download_result)
            else:
                page_result = None
                
            proc_result = {'download_result':download_result, 'page_result':page_result}
            result.append(proc_result)

            if download_result['code'] == 403:
                self.blocked_domain.append(domain)
                print '  detected a 403 domain [%s]' % domain
                # self.log.log_msg('  detected a 403 domain [%s]' % domain)
            else:
                if last_domain == domain:
                    time.sleep(2)
                last_domain = domain
                            
        return result

if __name__ == '__main__':
    obj = mega_crawler_task_proc('test', [], [], None, None)
    result = obj.download_page('http://www.goodshop.com/coupons/travelocity', [], 1 , [])
    print(result)
            
