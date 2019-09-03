import os
import sys

from conf import setting  # 导入配置文件
from lib.common import OpCase  # 导入读取用例的类

BASE_PATH = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))  # 获取ATP的路径
)
sys.path.insert(0, BASE_PATH)  # 将ATP目录下的所有文件加到环境变量，这样保证以后在哪里运行都可以


class CaseRun(object):
    def find_cases(self):
        op = OpCase()  # 实例化获取用例的类，便于调用OpCase()类下的函数
        for f in os.listdir(setting.CASE_PATH):  # 每次循环的时候读一个excel
            abs_path = os.path.join(setting.CASE_PATH, f)  # 拼成绝对路径，f只是一个文件名
            case_list = op.get_case(abs_path)  # 调用OpCase()类下的获取用例的函数，获取所有用例
            res_list = []
            pass_count, fail_count = 0, 0  # 设置初始的成功、失败用例个数
            for case in case_list:  # 循环每个excel里面所有用例
                # print(case)
                url, method, req_data, check = case
                print(check)
                res = op.my_request(url, method, req_data)  # 调用完接口返回的结果，res:实际结果
                status = op.check_res(res, check)  # 调用check_res()函数，校验预期结果&实际结果
                # print(res, status)
                res_list.append([res, status])  # 将返回结果和测试结果加入一个list，定义res_list,便于写入excel
                if status == '成功':
                    pass_count += 1
                else:
                    fail_count += 1
                # print(pass_count,fail_count)
                # self.pass_count = pass_count
                # self.fail_count = fail_count
            op.write_excel(res_list,pass_count,fail_count)  # 写入excel
            msg = '''
            xx你好：
                本次共运行%s条用例，通过%s条，失败%s条。
            ''' % (len(res_list), pass_count, fail_count)
            # sendmail('测试用例运行结果', content=msg, attrs=abs_path)  # 发送测试结果邮件


CaseRun().find_cases()
