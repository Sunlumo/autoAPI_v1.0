import logging
import os
from logging import handlers
from conf import setting


class MyLogger(object):
    def __init__(self, file_name, level='info', backCount=5, when='D'):
        logger = logging.getLogger()  # 先实例化一个logger对象，先创建一个办公室
        logger.setLevel(self.get_level(level))  # 设置日志的级别
        cl = logging.StreamHandler()  # 负责往控制台输出的人
        bl = handlers.TimedRotatingFileHandler(filename=file_name, when=when, interval=1, backupCount=backCount,
                                               encoding='utf-8')
        fmt = logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        cl.setFormatter(fmt)  # 设置控制台输出的日志格式
        bl.setFormatter(fmt)  # 设置文件里面写入的日志格式
        logger.addHandler(cl)
        logger.addHandler(bl)
        self.logger = logger  # 直接在这里实例化，用的时候就不用再实例化了

    def get_level(self, str):
        level = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warn': logging.WARNING,
            'error': logging.ERROR
        }
        str = str.lower()
        return level.get(str)


path = os.path.join(setting.LOG_PATH, setting.LOG_NAME)  # 拼好日志的绝对路径
atp_log = MyLogger(path, setting.LEVEL).logger  # 直接在这里实例化，用的时候就不用再实例化了
