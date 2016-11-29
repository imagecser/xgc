# -*- coding:utf-8 -*-
import cookielib
import urllib2
import urllib
import time
import os
import re
import uuid
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
maddr = ['lestdawn@163.com']
logfile, postfile = 'main.log', 'post.log'
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))


def get_th():
    itry = 0
    while True:
        global opener
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0')]
        # 构建CookieJar Opener
        try:
            cap_content = opener.open(capurl, timeout=10).read()
            open('image.jpg', 'wb').write(cap_content)
            capocr = image_to_string(Image.open('image.jpg'))
            cap = capocr.replace('\n', '').replace(' ', '')
            # 打开验证码网页，保存验证码，OCR转化
            data = urllib.urlencode({'IDToken1': '9405257',
                                     'IDToken2': 'nju697196',
                                     'inputCode': cap,
                                     'encoded': 'false'})
            html = opener.open(cerurl, data, timeout=10).read()
            itry += 1
            # 携带headers尝试登陆身份验证页面
            if len(html) > 2000:
                page = opener.open('http://xgc.nju.edu.cn/xg/main.psp', timeout=10).read()
                log(logfile, "Authentication for [%d] times" % itry, 'INFO')
                return page
                # 携带登陆成功的cookies,登陆TMD学工处主页，以字节数判断验证是否成功
            if itry >= 32:
                log(logfile, "Authentication for over [32] times. Quited.", 'WARNING')
                break
                # 登陆超过2**5次失败，暂时跳过，等待下一次重新尝试
        except:
            trace = traceback.format_exc()
            log(logfile, trace, 'ERROR')
            break
            # 错误返回traceback信息
    return ''


def rewrite(post_read):
    page = re.findall(re.compile('h.+htm'), post_read)
    # 匹配所有网址为list
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0')]
    for iurl in range(len(page)):
        try:
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
            name = str(uuid.uuid1())
            rewpath = 'C:\\inetpub\\wwwroot\\xgc\\c' + name + '.html'
            open(rewpath, 'w').write(rew)
            post_read = post_read.replace(page[iurl], 'http://www.icser.me/xgc/c' + name + '.html')
            time.sleep(0.1)
        except:
            log(logfile, page[iurl], 'ERROR')
    return post_read
    # 依次获得每个网页的源码，保留标题、所需的正文，填补并改善html格式，将超链接的相对路径换位绝对路径，
    # 将改写的网页存入网站服务器/xgc/，以uuid.uuid1()命名


def comp(page):
    finfo = open('info.txt', 'a')
    if page != '':
        page = etree.HTML(page)
        old, new = [o for o in open('info.txt', 'r')], []
        ltitle = page.xpath('//tr/td/ul/li/div/span/a/@title')
        lhref = page.xpath('//tr/td/ul/li/div/span/a/@href')
        for i in range(len(ltitle)):
            new.append(ltitle[i] + '\n')
            new.append('view-source: http://xgc.nju.edu.cn/xg/main.psp' +lhref[i] + '\n')
        res = [i for i in new if i not in old]
        finfo.writelines(res)
        return res
        # 构造新旧信息的list：旧[已存文件读取]，新[xpath从get_th()中获得]、list结构有改进空间，懒了
        # 比较得出新信息，将新信息写入，返回list
    else:
        return []


def join():
    post, pare = '', comp(get_th())
    # 构造空字符串post，待添加发送的信息；pare即返回的list
    if os.path.exists('post_temp.log'):
        post += open('post_temp.txt', 'r').read()
        os.remove('post_temp.txt')
        # 添加曾未发送的信息，删除暂时性文档
    for item in pare:
        post += item
    if post.replace(' ', '').replace('\n', '') != '':
        post = post.replace('\n\n', '\n')
        # 写入新信息，准备重写为外部网址
        post = rewrite(post)
        try:
            send_(maddr, post, u"学工园地更新动态")
            log(postfile, post, 'INFO')
        except:
            trace = traceback.format_exc()
            open('post_temp.txt', 'a').write(post)
            log(logfile, trace, 'ERROR')
            # 将未发送成功的信息暂时存储

if __name__ == "__main__":
    while True:
        try:
            join()
        except:
            trace = traceback.format_exc()
            log(logfile, trace, 'ERROR')
        finally:
            opener.close()

            time.sleep(1800)
