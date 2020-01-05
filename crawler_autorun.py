# -*- coding: utf-8 -*-
'''
Created on 2012-7-4

@author: Shen Min
'''

import sys
import os

def win_autorun(name, path):
    try:
        import win32api
        import win32con
    except ImportError:
        return True
    runpath = "Software\Microsoft\Windows\CurrentVersion\Run"
    hKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, runpath, 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(hKey, name, 0, win32con.REG_SZ, '"' + path + '"')
    win32api.RegCloseKey(hKey)
    return True

if __name__ == '__main__':
    win_autorun('test', 'c:\\test\\test.exe');