import time
import urllib
import urllib2
import cookielib

def DownloadFile(fileUrl):
    isDownOk=False
    try:
        if fileUrl:
            # imgurl = 'http://cer.nju.edu.cn/amserver/verify/image.jsp'
            urllib.urlretrieve(fileUrl,'D:\python\OCR\img\code.jpg')
            isDownOK=True
        else:
            print 'ERROR: fileUrl is NULL!'
    except:
        isDownOK=False

    return isDownOK

hosturl = 'http://cer.nju.edu.cn/amserver/UI/Login'
imgurl='http://cer.nju.edu.cn/amserver/verify/image.jsp'
url = 'http://cer.nju.edu.cn/amserver/UI/Login'

cookiejar=cookielib.CookieJar()
urlopener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
urllib2.install_opener(urlopener)
urlopener.addheaders.append(('User-Agent', 'Mozilla/5.0 (compatible; MISE 9.0; Windows NT 6.1); Trident/5.0'))
h = urllib2.urlopen(hosturl)

username = '9405257'
password = 'nju697196'
values={'encoded':'true','goto':'aHR0cDovL3dlYnBsdXMubmp1LmVkdS5jbi94Zy9tYWluLnBzcA==','gotoOnFail':'','IDToken0':'','IDButton':'Submit','IDToken1':username, 'IDToken2':password, 'inputCode':authcode,'gx_charset':'UTF-8'}
data=urllib.urlencode(values)

url_post = urllib2.Request(url,data)
print DownloadFile(imgurl)
authcode=raw_input('Please enter the authcode:')
urlcontent=urlopener.open(url_post)

print urlcontent.geturl()

# Make sure we are logged in
if not 'id' in [cookie.name for cookie in cookiejar]:
    print "Login failed with login=%s, password=%s, authcode=%s" % (username, password, authcode)
else:
    print 'We are logged in!'

page=urlcontent.read(500000)
print page