# app测试案例-成员
import basesys
import allure
import pytest

from pages.App.app import App
from utils.utils import Utils


# todo 数据封装
@allure.feature("成员管理-app端测试案例")
class TestWeWork:
    def setup_class(self):
        self.app = App()
        self.eles = Utils.get_data("../../datas/conf_data/eles_data.yaml")['App']['contact']['edit_member']

    def setup(self):
        self.app.start()

    def teardown(self):
        self.app.back(2)

    def teardown_class(self):
        self.app.stop()

    @allure.story("添加成员-快速输入")
    @allure.title("{title}")
    @pytest.mark.parametrize(
        "name1,mobile1,name2,mobile2,title",
        [
            [Utils.fake.name(), Utils.fake.mobile(), Utils.fake.name(), Utils.fake.mobile(), "添加成员1-保存并继续添加成员2-保存"]
        ]
    )
    def test_add_member_quick(self, name1, mobile1, name2, mobile2, title):
        with allure.step("启动app->主页->通讯录->添加成员->手动添加->选择快速输入->输入成员1姓名、手机号->保存并继续添加"):
            add_member = self.app.goto_main().click_contact().click_add_member_card()\
                .click_manual_add().choose_edit("快速输入").edit_member_quick(name1, mobile1).click_save_continue_button()

        with allure.step("验证弹出提示'添加成功'"):
            assert self.app.check_toast() == "添加成功"

        with allure.step("输入成员2姓名、手机号->保存"):
            add_member.edit_member_quick(name2, mobile2, invite=False).click_save_button()

        with allure.step("验证弹出提示'添加成功'"):
            assert self.app.check_toast() == "添加成功"

    @allure.story("添加成员-完整输入")
    @allure.title("{title}")
    @pytest.mark.parametrize(
        "data,title",
        [
            ({'name': Utils.fake.name(), 'mobile': Utils.fake.mobile(), 'gender': 2, 'address': '软件园'}, "填写必填项：（姓名，手机号），选填项：（性别，地址），添加成员成功"),
            ({'name': Utils.fake.name(), 'email': Utils.fake.email(), 'identity': True, 'department': '测试部'}, "填写必填项：（姓名，邮箱），选填项：（身份，部门），添加成员成功")
        ]
    )
    def test_add_member_full(self, data, title):
        with allure.step("启动app->主页->通讯录->添加成员->手动添加->选择完整输入->输入成员信息->保存"):
            self.app.goto_main().click_contact().click_add_member_card().click_manual_add()\
                .choose_edit("完整输入").edit_member_full(**data).click_save_button()

        with allure.step("验证弹出提示'添加成功'"):
            assert self.app.check_toast() == "添加成功"

    @allure.story("添加成员-反例-必填项校验")
    @allure.title("{title}")
    @pytest.mark.parametrize(
        "data,exp_tooltip,title",
        [
            ({'mobile': Utils.fake.mobile()}, "姓名不能为空", "缺少必填项（姓名），点击保存后弹出提示框，提示内容正确"),
            ({'name': Utils.fake.name()}, ["手机和邮箱不能同时为空", "手机号不能为空"], "手机号和邮箱均为空时，点击保存后弹出提示框，提示内容正确")
        ]
    )
    def test_add_member_false(self, data, exp_tooltip, title):
        with allure.step("启动app->主页->通讯录->添加成员->手动添加->输入成员信息->保存"):
            self.app.goto_main().click_contact().click_add_member_card().click_manual_add()\
                .edit_member_full(**data).click_save_button()

        with allure.step("验证弹出提示框，提示内容正确"):
            # todo 偶发asssert StaleElementReferenceException元素过期
            assert self.app.get_attribute(*self.app.x_ele(self.eles['tooltip']), 'text') in exp_tooltip

    # 单个删除成员，并验证通讯录中无已删除成员
    def test_delete_member_scene(self):
        # 点击成员名片,进入编辑界面
        self.edit_member = self.app.goto_main().click_contact().click_member_card().click_edit_member()
        # 获取成员姓名信息
        self.del_name = str(self.edit_member.member_name)
        self.del_ID = str(self.edit_member.member_ID)
        # 执行删除操作
        self.edit_member.delete_member()
        self.refresh_contacts(self.del_name)
        print(f'删除成员姓名为：{self.del_name}')
        print(f'删除成员ID为：{self.del_ID}')
        assert self.del_name not in self.contacts

    def refresh_contacts(self, name, n=8):
        i = 0
        while True:
            i += 1
            self.contacts = self.app.goto_main().click_contact().get_contacts()
            if i == n:
                # ❓1⃣️思路🤔：查询删除成员名字一直在列表中时，最后一次点击该名字成员进入编辑成员界面获取member_ID与删除成员ID比对
                # 若不一致，则重名，若无法点到编辑成员界面，则界面未刷新。
                # 注意操作后返回通讯录界面
                # 但成员较多时性能差❓
                print(f'⚠️已获取通讯录名单{n}次，若删除人员仍存在通讯录中，可能存在同名情况，请手工比对成员ID')
                break
            elif name in self.contacts:
                print(f'第{i}次获取通讯录列表')
                continue
            else:
                print(f'第{i}次获取通讯录列表')
                break

    # todo 需优化：忽略部门项+无可删除项结束，不报错
    # 批量删除n个成员,并验证删除后，通讯录中无已删除成员
    def _test_delete_members_scene(self, n=3):
        members = []
        del_message = {}
        for i in range(n):
            select_name = str(self.app.goto_main().click_contact().select_member().get_attribute('text'))
            if i == 0:
                name = None
            else:
                name = select_name
                print(f'删除上一成员返回通讯录页面首次定位的名字是：{name}')
            # 点击成员名片,进入编辑界面
            self.edit_member = self.app.goto_main().click_contact().click_member_card(name).click_edit_member()
            # 获取成员姓名信息
            self.del_name = str(self.edit_member.member_name)
            self.del_ID = str(self.edit_member.member_ID)
            print(f'删除成员姓名为：{self.del_name}')
            print(f'删除成员ID为：{self.del_ID}')
            members.append(self.del_name)
            del_message[self.del_name] = self.del_ID
            # 执行删除操作
            self.edit_member.delete_member()
        # print(f'删除成员名单为：{members}')
        self.refresh_contacts(self.del_name)    # ❓人多时性能较差，是否有更好方式等待页面刷新
        print(f'删除成员名单为：{del_message}')
        for member in members:
            assert member not in self.contacts
