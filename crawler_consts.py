# -*- coding: utf-8 -*-
'''
Created on 2012-5-18

@author: Shen Min
'''

import urllib

MEGA_CRAWLER_BUILD      = 37
MEGA_CRAWLER_DATE       = '2015.1.19'
MEGA_CRAWLER_VERSTRING  = 'Mega Crawler Client v1.0 (X-platform/python2.7), build %s(#%d)\nCopyright(c) 2012, Mega Information Technology Limited.' % (MEGA_CRAWLER_DATE, MEGA_CRAWLER_BUILD)
MEGA_CRAWLER_CLIENTVER  = urllib.urlencode({'client_version':'build %s(#%d)' % (MEGA_CRAWLER_DATE, MEGA_CRAWLER_BUILD)})