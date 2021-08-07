# xmind转csv
from xmindparser import xmind_to_dict
import csv


class XmindToCsv():

    def topics_num(self, value):
        """获取xmind标题个数"""
        try:
            return len(value['topics'])
        except KeyError:
            return 0

    def xmind_title(self, value):
        """获取xmind标题内容"""
        return value['title']

    def write_csv(self, filename, case):
        '''写入csv文件，case为列表'''
        headers = ["模块", "测试标题", "测试步骤", "预期结果"]

        with open(filename, 'w')as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(case)
        print("success!")

    def read_xmind(self, filename):
        '''读取xmind内容，返回case列表'''

        # xmind内容
        xmind_content = xmind_to_dict(filename)[0]['topic']
        # 模块内容
        module_name = self.xmind_title(xmind_content)
        # 二级模块的数量
        module_num = self.topics_num(xmind_content)
        # 用例列表
        case_list = []

        for i in range(module_num):
            case_num = self.topics_num(xmind_content['topics'][i])
            if case_num == 0:
                print('第{}个功能模块下，测试的功能点数量为0，请确认用例是否编写完成'.format(i + 1))
            else:
                tag = self.xmind_title(xmind_content['topics'][i])
                case_point_num = self.topics_num(xmind_content['topics'][i])
                for j in range(case_point_num):
                    case = []
                    if case_point_num == 0:
                        print('测试用例为空，请确认用例是否编写完成')
                    else:
                        case_point = self.xmind_title(xmind_content['topics'][i]['topics'][j])
                        case_step = self.xmind_title(xmind_content['topics'][i]['topics'][j]['topics'][0])
                        expected_result = self.xmind_title(xmind_content['topics'][i]['topics'][j]['topics'][0]['topics'][0])
                        case_title = "【" + tag + "】" + case_point
                        case.append(module_name)
                        case.append(case_title)
                        case.append(case_step)
                        case.append(expected_result)
                        case_list.append(case)
        return case_list

    def main(self, csv_file, xmind_file):
        case_list = self.read_xmind(xmind_file)
        self.write_csv(csv_file, case_list)


if __name__ == '__main__':
    xmind_file = "/Users/lusi/PycharmProjects/TestWeWork/testcases/功能测试案例/企业微信测试案例.xmind"
    csv_file = "/Users/lusi/PycharmProjects/TestWeWork/testcases/功能测试案例/企业微信测试案例.csv"
    XmindToCsv().main(csv_file, xmind_file)



