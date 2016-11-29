# coding: utf-8

import sys
import urllib2
import traceback
import cookielib
import chardet
import time
from lxml import etree
import uuid
reload(sys)
sys.setdefaultencoding('utf-8')

x = []
time1 = time.time()
for i in range(10000):
    x.append(uuid.uuid1())
print time.time() - time1