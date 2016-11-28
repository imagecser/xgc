# coding: utf-8

import sys
import urllib2
import traceback
import cookielib
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')

new = []
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
opener.addheaders = [
    ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0')]
url = 'file:///C:/Users/Administrator/Desktop/x.html'
page = etree.HTML(opener.open(url, timeout=10).read())
ltitle = page.xpath('//div/table/tbody/tr/td/ul/li/div/span/a/@title')
lhref = page.xpath('//div/table/tbody/tr/td/ul/li/div/span/a/@href')
for i in range(len(ltitle)):
    print ltitle[i]
    print lhref[i]

