# -*- coding: utf-8 -*-
'''
Created on 2012-6-22

@author: Shen Min
'''

from distutils.core import setup
import py2exe, sys

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 1, 'dll_excludes': ["mswsock.dll", "powrprof.dll"], 'packages': ["win32api", "win32con"]}},
    console = ['crawler_main.py'],
    zipfile = None,
)
