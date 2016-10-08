#coding=utf8
import os
import logging
import mimetypes
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
import json
import codecs
from xml.dom import minidom
import os
import logging.config

def get_module_path():
    return os.path.dirname(__file__)

def get_absolute_path(path):
    return os.path.join(os.path.dirname(__file__),path)

def send_mail(to_list, subject, body, format='plain', attachFileName=None):
    # if isinstance(body, unicode):
    #     body = str(body)
    fromMail = "812674168@qq.com"
    me = ("%s<" + fromMail + ">") % (Header("自动邮件通知", 'utf-8'),)

    outer = MIMEMultipart()

    # if not isinstance(subject, unicode): python3默认使用Unicode编码
    #     subject = unicode(subject)
    outer['Subject'] = subject
    outer['From'] = me
    outer['To'] = ";".join(to_list)
    outer["Accept-Language"] = "zh-CN"
    outer["Accept-Charset"] = "ISO-8859-1,utf-8"

    if attachFileName:
        ctype, encoding = mimetypes.guess_type(attachFileName)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(attachFileName, 'rb') as fp:
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(fp.read())

        encoders.encode_base64(msg)

        fileName = attachFileName[(attachFileName.rfind('/') + 1):]
        msg.add_header('Content-Disposition', 'attachment', filename=fileName)
        outer.attach(msg)

    textPart = MIMEText(body, format, 'utf-8')
    outer.attach(textPart)

    try:
        s = smtplib.SMTP('smtp.qq.com')
        # s.connect("")
        s.login("812674168", "yurdolniuolybbea")
        s.sendmail(outer['From'], to_list, outer.as_string())
        s.close()
        return True
    except Exception as e:
        logging.info('send email error',e)
        return False


def set_logconf():
    #获取的是相对于执行路劲的相对目录，如执行python a.python，则ppath是None
    ppath=os.path.dirname(__file__)

    #logging的配置
    logging.config.fileConfig(ppath+"/conf/log.prop" if ppath else "conf/log.prop")

if __name__=='__main__':
    set_logconf()
    send_mail(['zhengzhang23@creditease.cn'],'tt','body')