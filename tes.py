# coding: utf-8

import sys
import urllib2
import traceback
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://jw.nju.edu.cn/'
try:
    response = urllib2.urlopen(url)
    print response.read()
except:
    trace = traceback.format_exc()
    print trace
    print trace.count('timed out')