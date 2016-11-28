# -*- coding:utf-8 -*-
import cookielib
import urllib2
import urllib
import time
import os
import re
import traceback
from i_log import *
from i_send import *
from lxml import etree
from pytesser import *
from PIL import Image
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cerurl = 'http://cer.nju.edu.cn/amserver/UI/Login'
capurl = 'http://cer.nju.edu.cn/amserver/verify/image.jsp'
maddr= ['lestdawn@163.com']
logfile, postfile = 'main.log', 'post.log'
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))


def get_th():
    itry, iloginout, ivisitout, ivisitun, itwe = 0, 0, 0, 0, 0
    while True:
        global opener
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0')]
        try:
            cap_content = opener.open(capurl, timeout=10).read()
            open('image.jpg', 'wb').write(cap_content)
            capocr = image_to_string(Image.open('image.jpg'))
            cap = capocr.replace('\n', '').replace(' ', '')
            data = urllib.urlencode({'IDToken1': '9405257',
                                     'IDToken2': 'nju697196',
                                     'inputCode': cap,
                                     'encoded': 'false'})
            try:
                html = opener.open(cerurl, data, timeout=10).read()
                itry += 1
                if len(html) > 2000:
                    try:
                        page = opener.open('http://xgc.nju.edu.cn/xg/main.psp', timeout=10).read()
                        log(logfile, "Authentication for [%d] times" % itry, 'INFO')
                        return page
                    except:
                        trace = traceback.format_exc()
                        if trace.count('timed out') > 0:
                            ivisitout += 1
                            if ivisitout > 5:
                                log(logfile, '[xgc url] timed out\n' + trace, 'ERROR')
                                break
                        else:
                            ivisitun += 1
                            if ivisitun > 5:
                                log(logfile, '[xgc url] error unknown\n' + trace, 'ERROR')
                                break
                if ivisitout == 0:
                    if itry >= 20:
                        if itwe == 0:
                            log(logfile, "Authentication for over [20] times", 'WARNING')
                            itwe = 1
                    if itry >= 50:
                        log(logfile, "Authentication for over [50] times. Quited.", 'WARNING')
                        break
            except:
                trace = traceback.format_exc()
                if trace.count('timed out') > 0:
                    iloginout += 1
                    if iloginout > 5:
                        log(logfile, '[login url]\n' + trace, 'ERROR')
                        break
                    else:
                        continue
        except:
            trace = traceback.format_exc()
            log(logfile, '[captcha url]\n' + trace, 'ERROR')
            break
    return ''


def rewrite(post_read):
    icserpage = []
    page = re.findall(re.compile('h.+htm'), post_read)
    for iurl in range(len(page)):
        iresponse = opener.open(page[iurl]).read()
        iresponse = str(iresponse).replace('\n', '')
        ititle = re.findall('<html.+?</title>', iresponse)
        rew = re.sub('> +? <', '>\n<', ititle[0])
        ibody = re.findall('<div frag=.+?</div>.+?</div>.+?</td>', iresponse)
        rew += '\n' + re.sub('> +? <', '>\n<', ibody[1]) + '\n' + '</body></html>'
        rew = rew.replace('href="/',
                          'href="http://xgc.nju.edu.cn/').replace('src="/',
                                                                  'src="http://xgc.nju.edu.cn/').replace(
            "src='/", "src='http://xgc.nju.edu.cn/").replace("'src', '/", "'src', 'http://xgc.nju.edu.cn/")
        name = str(int(time.time()))
        rewpath = 'C:\Program Files\c' + name + '.html'
        open(rewpath, 'w').write(rew)
        post_read = post_read.replace(page[iurl], 'http://www.icser.me/xgc/c' + name + '.html')
    return post_read


def comp(page):
    if page != '':
        page = etree.HTML(page)
        open('info.txt', 'a')
        old, new = [o for o in open('info.txt', 'r')], []
        ltitle = page.xpath('//tr/td/ul/li/div/span/a/@title')
        lhref = page.xpath('//tr/td/ul/li/div/span/a/@href')
        for i in range(len(ltitle)):
            new.append(ltitle[i] + '\n')
            new.append('view-source: http://xgc.nju.edu.cn/xg/main.psp' +lhref[i] + '\n')
        res = [i for i in new if i not in old]
        open('info.txt', 'a').writelines(res)
        return res
    else:
        return []


def join():
    post, pare = '', comp(get_th())
    if os.path.exists('post_temp.log'):
        post += open('post_temp.log', 'r').read()
        os.remove('post_temp.log')
    for item in pare:
        post += item
    if post.replace(' ', '').replace('\n', '') != '':
        post = post.replace('\n\n', '\n')
        post = rewrite(post)
        try:
            send_(maddr, post, u"学工园地更新动态")
            log(postfile, post, 'INFO')
        except:
            trace = traceback.format_exc()
            open('post_temp.log', 'a').write(post)
            log(logfile, '[email sending]\n' + trace, 'ERROR')

if __name__ == "__main__":
    while True:
        try:
            join()
        except:
            trace = traceback.format_exc()
            log(logfile, trace, 'ERROR')
        finally:
            time.sleep(1800)
