# 接口测试案例-成员
import basesys
import allure
import pytest

from pages.API.user_api import User
from utils.utils import Utils


@allure.feature("成员管理-接口测试案例")
class TestUserAPI:
    with allure.step("载入测试数据"):
        create_data = Utils.get_data("../../datas/test_data/api/user/create_user.yaml")
        delete_data = Utils.get_data("../../datas/test_data/api/user/delete_user.yaml")
        update_data = Utils.get_data("../../datas/test_data/api/user/updata_user.yaml")

    def setup_class(self):
        # 获取token参数
        with allure.step("获取access_token"):
            token_data = Utils.get_data("../../datas/conf_data/access_token_api.yaml")
            corp_id = token_data["ID"]["Test"]
            corp_secret = token_data["SECRET"]["Contact"]
        # 实例化成员类
        with allure.step("实例化成员类"):
            self.user = User(corp_id, corp_secret)

        # 清理更新成员测试环境并预埋待更新数据数据
        with allure.step("清理更新成员测试环境并预埋待更新数据数据"):
            self.user.batch_delete_users(['DaiGengXin', 'Scene1'])
            self.init_data(self, self.update_data['create'])
            self.user.create_user(**self.update_data['create'])

    @allure.story("成员管理-业务场景案例")
    @allure.title(
        "创建成员-读取-列表-详情列表-更新成员-读取-列表-详情列表-删除成员-读取-列表-详情列表"
    )
    def test_user_scene1(self):
        """
        1、创建成员，断言errcode=0✅
        2、读取成员，errcode=0,name,department,address，mobile,email正确✅
        3、获取部门成员列表，errcode=0,name,department正确✅
        4、获取部门成员详情列表，errcode=0,name,department,address，mobile,email正确✅
        5、更新并增加成员归属部门，更新address，mobile✅
        6、读取成员，errcode=0,name,email不变，department,address，mobile更新正确✅
        7、获取部门成员列表，errcode=0,name不变,department更新正确✅
        8、获取部门成员详情列表，errcode=0,name,email不变，department,address，mobile更新正确✅
        9、删除成员,断言errcode=0✅
        10、读取成员，errcode=60111✅
        11、获取部门成员列表，errcode=0,,userid不存在列表中✅
        12、获取部门成员详情列表，errcode=0,userid不存在列表中✅
        """
        with allure.step("初始化测试数据"):
            data = Utils.get_data("../../datas/test_data/api/user/scene_test.yaml")['scene1']
            c_data: dict = self.init_data(data['create'])
            u_data = self.init_data(data['update'])
            d_id = c_data['userid']
            print(f"创建成员入参：{c_data}")
            print(f"待更新成员入参：{u_data}")
            print(f"待删除成员id为：{d_id}")

        # 创建成员
        with allure.step("创建成员"):
            r = self.user.create_user(**c_data)
            print(r)
        with allure.step("创建成员成功"):
            assert r['errcode'] == 0

        # 读取成员
        with allure.step("读取成员"):
            r = self.user.get_user(d_id)
            print(r)
        with allure.step("读取成员成功"):
            assert r['errcode'] == 0
        with allure.step("读取成员获得的name,department,address，mobile,email与所创建的成员信息一致"):
            for i in c_data:
                assert r[i] == c_data[i]

        # 获取部门成员列表
        with allure.step("获取部门成员列表"):
            r = self.user.get_simple_list(1, 1)
            print(r)
        with allure.step("获取部门成员列表成功"):
            assert r['errcode'] == 0
        with allure.step("获取部门成员列表中该userid的name,department与所创建的成员信息一致"):
            user_list = r['userlist']
            for i in user_list:
                if i['userid'] == d_id:
                    assert i['name'] == c_data['name']
                    assert i['department'] == c_data['department']
                    break

        # 获取部门成员详情列表
        with allure.step("获取部门成员详情列表"):
            r = self.user.get_list(1, 1)
            print(r)
        with allure.step("获取部门成员详情列表成功"):
            assert r['errcode'] == 0
        with allure.step("获取部门成员详情列表中该userid的name,department,address，mobile,email与所创建的成员信息一致"):
            user_list = r['userlist']
            for i in user_list:
                if i['userid'] == d_id:
                    for j in c_data:
                        assert i[j] == c_data[j]
                    break

        # 更新成员
        with allure.step("更新成员"):
            r = self.user.updata_user(**u_data)
            print(r)
        with allure.step("更新成员成功"):
            assert r['errcode'] == 0

        # 读取成员
        with allure.step("读取成员"):
            r = self.user.get_user(d_id)
            print(r)
        with allure.step("读取成员成功"):
            assert r['errcode'] == 0
        with allure.step("读取成员获得的name,email不变，department,address，mobile更新正确"):
            for i in u_data:
                if u_data[i] is None:
                    assert r[i] == c_data[i]
                else:
                    assert r[i] == u_data[i]

        # 获取部门成员列表
        with allure.step("获取部门成员列表"):
            r = self.user.get_simple_list(1, 1)
            print(r)
        with allure.step("获取部门成员列表成功"):
            assert r['errcode'] == 0
        with allure.step("获取部门成员列表中该userid的name不变,department更新正确"):
            user_list = r['userlist']
            for i in user_list:
                if i['userid'] == d_id:
                    assert i['name'] == c_data['name']
                    assert i['department'] == u_data['department']
                    break

        # 获取部门成员详情列表
        with allure.step("获取部门成员详情列表"):
            r = self.user.get_list(1, 1)
            print(r)
        with allure.step("获取部门成员详情列表成功"):
            assert r['errcode'] == 0
        with allure.step("获取部门成员详情列表中该userid的name,email不变，department,address，mobile更新正确"):
            user_list = r['userlist']
            for i in user_list:
                if i['userid'] == d_id:
                    for j in u_data:
                        if u_data[j] is None:
                            assert i[j] == c_data[j]
                        else:
                            assert i[j] == u_data[j]
                    break

        # 删除成员
        with allure.step("删除成员"):
            r = self.user.delete_user(d_id)
            print(r)
        with allure.step("删除成员成功"):
            assert r['errcode'] == 0

        # 读取成员
        with allure.step("读取成员"):
            r = self.user.get_user(d_id)
            print(r)
        with allure.step("读取失败，errcode=60111，UserID不存在"):
            assert r['errcode'] == 60111

        # 获取部门成员列表
        with allure.step("获取部门成员列表"):
            r = self.user.get_simple_list(1, 1)
            print(r)
        with allure.step("获取部门成员列表成功"):
            assert r['errcode'] == 0
        with allure.step("获取部门成员列表中该userid不存在"):
            user_list = r['userlist']
            userid_list = []
            for i in user_list:
                userid_list.append(i['userid'])
            assert d_id not in userid_list

        # 获取部门成员详情列表
        with allure.step("获取部门成员详情列表"):
            r = self.user.get_list(1, 1)
            print(r)
        with allure.step("获取部门成员详情列表成功"):
            assert r['errcode'] == 0
        with allure.step("获取部门成员详情列表中该userid不存在"):
            user_list = r['userlist']
            userid_list = []
            for i in user_list:
                userid_list.append(i['userid'])
            assert d_id not in userid_list

    @allure.story("创建成员")
    @allure.title("{title}")
    @pytest.mark.parametrize("title,exp_code,data", create_data)
    def test_create_user(self, title, exp_code, data):
        # 初始化测试数据
        self.init_data(data)

        with allure.step("调用创建成员接口"):
            # 创建成员
            r = self.user.create_user(**data)
            print(r)

        with allure.step("断言返回码与预期一致"):
            # 判断创建成员成功
            assert r['errcode'] == exp_code

    @allure.story("更新成员")
    @allure.title("{title}")
    @pytest.mark.parametrize("title,exp_code,data", update_data['update'])
    def test_update_user(self, title, exp_code, data):
        # 初始化测试数据
        self.init_data(data)

        with allure.step("调用更新成员接口"):
            r = self.user.updata_user(**data)

        with allure.step("断言返回码与预期一致"):
            assert r['errcode'] == exp_code

    @allure.story("读取成员")
    @allure.title("读取成员id为{id}的成员详细信息")
    @pytest.mark.parametrize("id", ['LuSi'])
    def test_get_user(self, id):
        with allure.step(f"调用读取成员接口，读取成员id为{id}的成员详细信息"):
            r = self.user.get_user(id)
            print(r)
        with allure.step("断言返回码与预期一致"):
            assert r['errcode'] == 0

    @allure.story("获取部门成员详情")
    @allure.title("获取部门编号为：{id}的所有成员详情列表")
    @pytest.mark.parametrize("id", [1, 10086])
    def test_get_list(self, id):
        # 获取部门成员详情列表
        with allure.step(f"调用接口，获取部门编号为：{id}的所有成员详情列表"):
            r = self.user.get_list(id)
            print(r)
        # 判断获取成功
        with allure.step("断言返回码与预期一致"):
            assert r['errcode'] == 0

    @allure.story("获取部门成员")
    @allure.title("获取部门编号为：{id}的所有成员列表")
    @pytest.mark.parametrize("id", [1, 10086])
    def test_get_sample_list(self, id):
        # 获取部门成员列表
        with allure.step(f"调用接口，获取部门编号为：{id}的所有成员列表"):
            r = self.user.get_simple_list(id)
            print(r)
        # 判断获取成功
        with allure.step("断言返回码与预期一致"):
            assert r['errcode'] == 0

    @allure.story("删除成员")
    @allure.title('{title}')
    @pytest.mark.parametrize("id, exp_errcode, title", delete_data['delete'])
    def test_delete_user(self, id, exp_errcode, title):
        if id == "DaiShanChu":
            # 正例预埋数据
            with allure.step("预埋数据(创建待删除成员)"):
                before_data = self.delete_data['create']
                r = self.user.create_user(**before_data)
                print(r)
            with allure.step("断言创建成功"):
                assert r['errcode'] == 0

        # 删除成员
        with allure.step(f"调用删除成员接口，删除成员id为{id}"):
            r = self.user.delete_user(id)
            print(r)
        # 判断删除成功
        with allure.step("断言返回码与预期一致"):
            assert r['errcode'] == exp_errcode

    def _test_clear_user_datas(self, n=1):
        # 清理测试环境，删除部门id为n的部门所有成员
        self.user.clear_user_datas(n)

    def init_data(self, data):
        with allure.step("随机生成测试数据,并初始化测试数据"):
            fake_data = {
                "userid": Utils.fake.userid(),
                "name": Utils.fake.name(),
                "mobile": Utils.fake.mobile(),
                "email": Utils.fake.email(),
                "address": Utils.fake.address()
            }
        # 如果yaml测试文件数据中未传入fake_data中的keys，data中插入初始化的随机参数
        for i in fake_data:
            if i not in data.keys():
                data[i] = fake_data[i]
        return data


# if __name__ == '__main__':
#     pytest.main(['test_user_api.py', '-vs'])
