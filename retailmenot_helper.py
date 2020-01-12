# -*- coding: utf-8 -*-
'''
Created on 2014-4-21

@author: Li Wei
'''

import time, urllib2, urllib, re, os, sys
from deathbycaptcha import SocketClient
from ctypes import *
import crawler_utils

g_deathbycaptcha_instance = None
g_deathbycaptcha_log = None

def get_blocked_page(url, content, response_url, useragent, retry):
    result = {'code':0, 'header':'', 'content': '', 'url':url, 'newurl':''}
    global g_deathbycaptcha_log
    if g_deathbycaptcha_log is None:
        g_deathbycaptcha_log = [0,0,0,0,0]
    t = time.time()
    x = g_deathbycaptcha_log[0]
    if t - x <= 3600:
        result['code'] = 403
        result['content'] = 'deathbycaptcha overload'
        return result
    g_deathbycaptcha_log.pop(0)
    g_deathbycaptcha_log.append(t)
    if useragent == '':
        addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36')]
    else:
        addheaders = [('User-agent', useragent)]
    fname = crawler_utils.get_run_dir() + '/tmp_img.jpg'
    m = re.match('.*?iframe src="(.*?)"', content, re.DOTALL | re.MULTILINE)
    global g_deathbycaptcha_instance
    if g_deathbycaptcha_instance is None:
        print "create deathbycaptcha instance"
        g_deathbycaptcha_instance = SocketClient('mega001', 'ike001')
        g_deathbycaptcha_instance.is_verbose = True
        print 'balance is %s US cents' % g_deathbycaptcha_instance.get_balance()
    if m:
        uri = m.groups(0)[0]
        opener = urllib2.build_opener()
        opener.addheaders = addheaders
        print uri
        f = opener.open(fullurl = uri, timeout = 15)
        page = f.read()
        #print page
        m = re.match('.*?src="(image\?c=(.*?))"', page, re.DOTALL | re.MULTILINE)
        if m:
            img_uri = 'http://api.recaptcha.net/' + m.groups(0)[0]
            print img_uri
            challenge_field = m.groups(0)[1]
            opener = urllib2.build_opener()
            opener.addheaders = addheaders
            f = opener.open(fullurl = img_uri, timeout = 15)
            img_content = f.read()
            if img_content:
                f = file(fname, "wb")
                f.write(img_content)
                f.close()
                response_field = g_deathbycaptcha_instance.decode(fname, 60);
                print response_field
                if response_field:
                    opener = urllib2.build_opener()
                    opener.addheaders = addheaders
                    data = urllib.urlencode({'action': 'process', 'recaptcha_challenge_field' : challenge_field, 'recaptcha_response_field' : response_field['text']})
                    f = opener.open(fullurl = response_url, data=data, timeout = 15)
                    result = {'code':f.getcode(), 'header':f.headers, 'content': f.read(), 'url':url, 'newurl':f.geturl()}
                    if re.match('.*?api\.recaptcha\.net/challenge', result['content'], re.DOTALL | re.MULTILINE):
                        retry = retry - 1
                        if retry == 0:
                            result['code'] = 403
                            return result
                        else:
                            return get_blocked_page(url, content, response_url, useragent, retry)
                    return result
    return result

if __name__ == '__main__':
    url = 'http://www.retailmenot.com/view/bluehost.com'
    content = '''processing(1): http://www.savings.com/deal/mobile_popup.ajax?id=2616273... <!doctype html><!--[if lte IE 7]> <html class="no-js ie7 oldie" lang="en"> <![endif]--><!--[if IE 8]> <html class="no-js ie8 oldie" lang="en"> <![endif]--><!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]--> <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# retailmenot: http://ogp.me/ns/fb/retailmenot#"> <meta charset="utf-8" /> <title>RetailMeNot: Coupon Codes, Coupons, Promo Codes, Free Shipping and Discounts for Thousands of Stores</title> <meta name="description" content="Find and share coupon codes and promo codes for great discounts at thousands of online stores." /> <meta property="fb:app_id" content="199633336744629" /><meta property="fb:admins" content="100001343531499" /><meta property="og:title" content="RetailMeNot.com Coupon Codes and Discounts" /><meta property="og:type" content="website" /><meta property="og:url" content="http://www.retailmenot.com/" /><meta property="og:image" content="http://o.rmncdn.com/gui/im/bigR.jpg" /><meta property="og:site_name" content="RetailMeNot.com" /><meta property="og:description" content="Find and share the latest coupon codes for great discounts at thousands of online stores!" /> <meta itemprop="image" content="http://o.rmncdn.com/gui/im/bigR.jpg" /> <meta name="keywords" content="coupon codes, code, discounts, coupons, promotional, promo, promotion, deal" /> <meta name="googlebot" content="noarchive" /> <meta name="format-detection" content="telephone=no"/> <meta name="viewport" content="width=1024" /> <meta name="msapplication-config" content="IEconfig.php" /> <link rel="apple-touch-icon" sizes="152x152" href="http://o.rmncdn.com/gui/im/apple-touch-icon-152.png" /> <link rel="apple-touch-icon" sizes="144x144" href="http://o.rmncdn.com/gui/im/apple-touch-icon-144.png" /> <link rel="apple-touch-icon-precomposed" sizes="120x120" href="http://o.rmncdn.com/gui/im/apple-touch-icon-120.png" /> <link rel="apple-touch-icon-precomposed" sizes="114x114" href="http://o.rmncdn.com/gui/im/apple-touch-icon-114.png"> <link rel="apple-touch-icon" sizes="76x76" href="http://o.rmncdn.com/gui/im/apple-touch-icon-76.png" /> <link rel="apple-touch-icon" sizes="72x72" href="http://o.rmncdn.com/gui/im/apple-touch-icon-72.png" /> <link rel="apple-touch-icon-precomposed" href="http://o.rmncdn.com/gui/im/apple-touch-icon-57.png"> <script type="text/javascript">
        var _gaq = _gaq || [];
        _gaq.push(['_setAccount','UA-54628-3']);
                _gaq.push(['_setCustomVar', 2, 'User Type', 'Anonymous', 3]);
                    _gaq.push(['_trackPageview']);
        
        (function() {
            var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
            ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
            var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
        })();
    </script> <link rel="stylesheet" type="text/css" href="http://o.rmncdn.com/gui/build/css/default-391e9a9a.min.css" /> <link rel="shortcut icon" type="image/ico" href="/favicon.ico" /> <link rel="canonical" href="http://www.retailmenot.com/" /> </head> <body> <style> #wrapper { width: 600px; } #content { width: 558px; } </style> <div id="wrapper" > <div id="content"> <img src="http://o.rmncdn.com/gui/im/logo.png" alt="RetailMeNot" /> <h1>Please verify that you are human...</h1> <p>We're sorry but your usage of this site resembles automated software. To protect our community we require that you verify your identity. To continue, please type the words that appear in the image below:</p> <form method="post"> <input type="hidden" name="action" value="process"/> <input type="hidden" name="url" value="/view/bluehost.com"/> <script type="text/javascript" src="http://api.recaptcha.net/challenge?k=6Le7-QsAAAAAAAHStfvQ2JQS4EljJdTNlFfu_n8N"></script><noscript> <iframe src="http://api.recaptcha.net/noscript?k=6Le7-QsAAAAAAAHStfvQ2JQS4EljJdTNlFfu_n8N" height="300" width="500" frameborder="0"></iframe><br/> <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea> <input type="hidden" name="recaptcha_response_field" value="manual_challenge"/></noscript> <input class="btn lg green" type="submit" /> </form> <p>We investigate every case of this nature and apologise in advance if you are a regular user of our services: <em>116.226.83.255</em></p> <p>If you feel that you have reached this page in error, please do not hesitate to <a href="/contact/blocked_user_report.php">contact us</a>.</p> </div> </div> </body></html>'''
    r = get_blocked_page(url, content, 'http://www.retailmenot.com/humanCheck.php', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36', 2)
    print r['code']
    f = file(os.path.join(os.path.dirname(__file__), 'response.dump.html'), "wb")
    f.write(r['content'])
    f.close()