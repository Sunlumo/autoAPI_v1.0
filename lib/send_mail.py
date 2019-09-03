import yagmail

from conf import setting
from lib.log import atp_log


def sendmail(title, content, attrs=None):
    # 以下邮箱的配置直接写在setting中，方便管理修改
    m = yagmail.SMTP(host=setting.MAIL_HOST,
                     user=setting.MAIL_USER,
                     password=setting.MAIL_PASSWRD,  # 邮箱的授权码
                     smtp_ssl=True)  # QQ邮箱时需要添加smtp_ssl=True
    m.send(to=setting.TO, subject=title,
           contents=content,
           attachments=attrs)
    atp_log.info('发送邮件完成')
