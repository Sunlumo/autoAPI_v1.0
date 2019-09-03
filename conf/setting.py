import os

BASE_PATH = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))  # 获取ATP所在的路径
)
MAIL_HOST = 'smtp.qq.com'
MAIL_USER = 'daishuai@onlinesign.com.cn'
MAIL_PASSWRD = '***32432'  # 授权码
TO = [
    '758588590@qq.com',  # 收件人
]
LEVEL = 'debug'  # 默认日志级别

LOG_PATH = os.path.join(BASE_PATH, 'logs')  # 存放日志的路径
CASE_PATH = os.path.join(BASE_PATH, 'cases')  # 存放日志的路径
LOG_NAME = 'atp.log'  # 日志的文件名
TEST_MAN = "shuai"
