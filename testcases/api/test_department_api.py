# 接口测试案例-部门
import basesys
import allure
import pytest

from pages.API.department_api import Department
from utils.utils import Utils


@allure.feature("部门管理-接口测试案例")
class TestDepartment:
    with allure.step("载入测试数据"):
        create_data = Utils.get_data("../../datas/test_data/api/department/create_department.yaml")

    def setup_class(self):
        # 获取token参数
        with allure.step("获取access_token"):
            token_data = Utils.get_data("../../datas/conf_data/access_token_api.yaml")
            corp_id = token_data["ID"]["Test"]
            corp_secret = token_data["SECRET"]["Contact"]
        # 实例化部门类
        with allure.step("实例化成员类"):
            self.department = Department(corp_id, corp_secret)

        with allure.step("清理测试环境"):
            self.department.delete_department(self.create_data[0][0]["id"])

    @allure.story("创建部门")
    @allure.title("{title}")
    @pytest.mark.parametrize("data, exp_errcode, title", create_data)
    def test_create_data(self, data, exp_errcode, title):
        print(data)
        r = self.department.create_department(data)
        print(r)
        assert r['errcode'] == exp_errcode

    @allure.story("获取部门列表")
    def test_get_department_list(self):
        r = self.department.get_department_list()
        print(r)
