# -*- coding: utf-8 -*-
'''
Created on 2012-5-28

@author: Shen Min
'''

import codecs, os, time
import crawler_utils

class mega_crawler_log:
    def __init__(self, crawler_id):
        self.__fileA = crawler_utils.get_run_dir() + '/crawler.log'
        self.__fileB = crawler_utils.get_run_dir() + '/crawler.0.log'
        self.__crawler_id = crawler_id
        self.__c = 0
        
    def __check_file_size(self):
        if os.path.isfile(self.__fileA):
            try:
                fs = os.path.getsize(self.__fileA)
            except:
                fs = 0L
                
            while fs >= 500000000L:
                try:
                    if os.path.isfile(self.__fileB):
                        os.remove(self.__fileB)
                except:
                    pass
                
                try:
                    os.rename(self.__fileA, self.__fileB)
                except:
                    pass

                if not os.path.isfile(self.__fileA):
                    fs = 0L
                else:
                    try:
                        fs = os.path.getsize(self.__fileA)
                    except:
                        fs = 0L

    def log_msg(self, msg):
        f = codecs.open(self.__fileA, 'a', 'utf-8')
        f.writelines('[%s][%s] - %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), self.__crawler_id, msg))
        f.close()
        self.__c += 1;
        
        if self.__c >= 20:
            self.__check_file_size()
            self.__c = 0
        

