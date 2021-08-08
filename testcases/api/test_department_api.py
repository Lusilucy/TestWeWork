# 接口测试案例-部门
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.abspath(os.path.dirname(curPath) + os.path.sep + "..")
sys.path.append(curPath)
import allure
import pytest
sys.path.append(rootPath)
from pages.API.department_api import Department
from utils.utils import Utils
print(sys.path)


class TestDepartment:
    create_data = Utils.get_data("./datas/test_data/contact/department/create_department.yaml")

    def setup_class(self):
        # 获取token参数
        token_data = Utils.get_data("./datas/conf_data/access_token_api.yaml")
        corp_id = token_data["ID"]["Test"]
        corp_secret = token_data["SECRET"]["Contact"]
        # 实例化部门类
        self.department = Department(corp_id, corp_secret)

    def setup(self):
        pass

    def teardown(self):
        pass

    @allure.title("{title}")
    @pytest.mark.parametrize("data, exp_errcode, title", create_data)
    def test_create_data(self, data, exp_errcode, title):
        if data['name'] == "测试部":
            self.department.delete_depatment(10086)
        print(data)
        r = self.department.create_department(data)
        print(r)
        assert r['errcode'] == exp_errcode

    def test_get_department_list(self):
        r = self.department.get_department_list()
        print(r)
