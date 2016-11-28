# coding: utf-8
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def send_(addr, msge, title):
    mailinfo = {
        "from": "lestdawn@qq.com",
        "to": ','.join(addr),
        "hostname": "smtp.qq.com",
        "username": "975909687",
        "password": "qfvfuxlxncldbahj",
        "mailsubject": title,
        "mailtext": msge,
        "mailencoding": "utf-8"
        }
    smtp = SMTP_SSL(mailinfo["hostname"])
    smtp.set_debuglevel(1)
    smtp.ehlo(mailinfo["hostname"])
    smtp.login(mailinfo["username"], mailinfo["password"])
    msg = MIMEText(mailinfo["mailtext"], 'plain', _charset='utf-8')
    msg["Subject"] = Header(mailinfo["mailsubject"], charset='utf-8')
    msg["from"] = mailinfo["from"]
    msg["to"] = mailinfo["to"]
    smtp.sendmail(mailinfo["from"], addr, msg.as_string())
    smtp.quit()
