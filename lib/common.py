import requests
import xlrd
from xlutils import copy

from conf import setting
from lib.log import atp_log


class OpCase(object):
    def get_case(self, file_path):
        cases = []  # 存放所有的case
        if file_path.endswith('.xls') or file_path.endswith('.xlsx'):  # 判断文件是否为excel文件
            try:  #
                book = xlrd.open_workbook(file_path)  # 打开excel
                sheet = book.sheet_by_index(0)  # 获取sheet页
                for i in range(1, sheet.nrows):  # 循环每一行
                    row_data = sheet.row_values(i)  # 获取每一行数据
                    cases.append(row_data[3:7])  # 将第5-8列的数据添加到case中
                atp_log.info('共读取%s条用例' % (len(cases)))  # 一共有多少条测试用例
                self.file_path = file_path  # 实例化file_path
            except Exception as e:
                atp_log.error('【%s】用例获取失败，错误信息：%s' % (file_path, e))
        else:  # 如果文件不是excel，提示
            atp_log.error('用例文件不合法的，%s' % file_path)
        return cases  # 返回case

    def dataToDict(self, data):
        # 把数据转成字典
        res = {}
        data = data.split(',')
        for d in data:
            # a=
            k, v = d.split('=')
            res[k] = v
        return res

    def my_request(self, url, method, data):  # 参数url,method,data
        method = method.upper()  # 传入参数有可能会有大小写，统一转成大写字母
        data = self.dataToDict(data)  # 将获取的数据做处理，转成字典
        try:
            if method == 'POST':  # 判断method的类型
                res = requests.post(url, data).text  # 发送请求并转换成字典
            elif method == 'GET':
                res = requests.get(url, params=data).text
            else:
                atp_log.warning('该请求方式暂不支持。。')  # 调用日志文件
                res = '该请求方式暂不支持。。'
        except Exception as e:
            msg = '【%s】接口调用失败，%s' % (url, e)
            atp_log.error(msg)
            res = msg
        return res  # 返回请求返回的内容

    def check_res(self, res, check):
        # res = res.replace('": "', '=').replace('": ', '=')  # 两次替换，把res里返回的字典里所有的替成=号（因为返回的Json串格式都是一样的)
        print("-----------", res)
        for c in check.split(','):  # 将预期结果里的以逗号分开
            if c not in res:  # 判断预期结果里的list是否在返回结果res里
                atp_log.info('结果校验失败，预期结果：【%s】，实际结果【%s】' % (c, res))
                return '失败'
        return '成功'

    def write_excel(self, cases_res, pass_count, fail_count):
        # [ ['dsfd',"通过"] ,['sdfsdf','失败'] ]
        book = xlrd.open_workbook(self.file_path)  # 打开excel
        new_book = copy.copy(book)  # 复制excel
        sheet = new_book.get_sheet(0)
        row = 1
        # print(pass_count)
        for case_case in cases_res:  # 将获取的写回excel
            sheet.write(row, 7, case_case[0])  # 写第9列
            sheet.write(row, 8, case_case[1])  # 写第10列
            sheet.write(row, 9, setting.TEST_MAN)
            sheet.write(row, 10, pass_count)
            row += 1
        new_book.save(self.file_path.replace('xls', 'xls'))  # 将xlsx格式转换成xls
