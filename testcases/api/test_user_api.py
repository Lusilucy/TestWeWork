import allure
import pytest

from pages.API.user_api import User
from utils.utils import Utils


class TestUserAPI:
    delete_data = Utils.get_data("../../datas/test_data/contact/user/delete_user.yaml")

    def setup_class(self):
        # 获取token参数
        token_data = Utils.get_data("../../datas/conf_data/access_token_api.yaml")
        corp_id = token_data["ID"]["Test"]
        corp_secret = token_data["SECRET"]["Contact"]
        # 实例化成员类
        self.user = User(corp_id, corp_secret)

    def setup(self):
        pass

    def teardown(self):
        pass

    # @pytest.mark.parametrize(
    #     "data",
    #     [{
    #         "name": f'{Utils.fake.name()}',
    #         "userid": Utils.fake.userid(),
    #         "mobile": Utils.fake.mobile(),
    #         "department": 3
    #     }]
    # )
    def test_create_user(self):
        # 实例化创建成员数据
        data = {
            # todo 优化实例数据，或可以另外存储yaml?，parametrice参数化
            "name": f'{Utils.fake.name()}',
            "userid": Utils.fake.userid(),
            "mobile": Utils.fake.mobile(),
            "department": 1,
            # "is_leader_in_dept": 0,
            # "address": Utils.fake.address,
            # "gender": Utils.fake.gender,
            # "main_department": None
            # "alias": "djoalj joifa"
            # "avatar_mediaid": 1111
            # "enable": 3222222222
            # "to_invite": "^%1&#$"
            # "order": 33
            # "external_position": "一二三四五六七八九十十一十二"
        }
        # todo 优化数据模版
        create_data = Utils.get_data("../../datas/test_data/contact/user/create_user.json", data)
        print(create_data)
        # 创建成员
        r = self.user.create_user(create_data)
        print(r)
        # 判断创建成员成功
        assert r['errcode'] == 0

    def test_get_user(self):
        r = self.user.get_user('LuSi')
        print(r)
        assert r['errcode'] == 0

    @pytest.mark.parametrize("id", [1, 3])
    def test_get_list(self, id):
        # 获取部门成员详细列表
        r = self.user.get_list(id)
        print(r)
        # 判断获取成功
        assert r['errcode'] == 0

    @pytest.mark.parametrize("id", [1, 3])
    def test_get_sample_list(self, id):
        # 获取部门成员列表
        r = self.user.get_simple_list(id)
        print(r)
        # 判断获取成功
        assert r['errcode'] == 0

    @allure.title('{title}')
    @pytest.mark.parametrize("id, exp_errcode, title", delete_data['delete'])
    def test_delete_user(self, id, exp_errcode, title):
        if id == "DaiShanChu":
            # 正例预埋数据
            before_data = Utils.get_data("../../datas/test_data/contact/user/create_user.json", self.delete_data['create'])
            r = self.user.create_user(before_data)
            assert r['errcode'] == 0

        # 删除成员
        r = self.user.delete_user(id)
        print(r)
        # 判断删除成功
        assert r['errcode'] == exp_errcode

    def _test_clear_user_datas(self, n=3):
        # 清理测试环境，删除所有部门成员
        self.user.clear_user_datas(n)

    def _test_update_user(self):
        # todo 测试update_user，并思考与create_user创建联动数据模版
        pass

# todo 业务串联案例
# todo 单功能案例 -> 正反例测试


# if __name__ == '__main__':
#     pytest.main(['test_user_api.py', '-vs'])
