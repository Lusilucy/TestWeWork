# web测试案例-成员
from time import sleep

from selenium.webdriver.common.by import By
import allure

from pages.Web.login_page import LoginPage
from utils.utils import Utils


@allure.feature("成员管理")
class TestUserweb:
    def setup_class(self):
        with allure.step("登录首页"):
            self.login = LoginPage()

    def setup(self):
        pass

    def teardown(self):
        pass

    def teardown_class(self):
        self.login.quit()

    @allure.story("成员管理-业务场景案例")
    @allure.title("添加成员-保存并继续-添加成员-保存")
    def test_add_member_scene(self):
        self.login.logging("-------------------------------- test_add_member_scene 开始 --------------------------------")
        with allure.step(
            "1、点击通讯录进入通讯录界面；\n"
            "2、点击页面上部添加成员按钮进入添加成员页面；\n"
            "3、输入成员姓名、帐号、手机号；"
        ):
            # 初始化成员1数据
            member1 = Utils.member_data()
            print(member1)
            self.login.logging(f"--------member2:{member1[0], member1[1], member1[2]}--------")
            add_member1 = self.login.switch_index().click_contact_button().click_add_member_button()\
                .add_member(member1[0], member1[1], member1[2])

        with allure.step("4、点击保存并继续按钮添加按钮；"):
            add_conticue = add_member1.click_save_and_continue_button()

        with allure.step("5、断言页面停留在当前编辑界面；"):
            assert add_conticue.get_page_title_text() == "添加成员"

        with allure.step("6、添加第二个成员，输入成员信息：姓名，帐号，邮箱；"):
            # 初始化成员2数据
            member2 = Utils.member_data()
            print(member2)
            self.login.logging(f"--------member2:{member2[0], member2[1], member2[3]}--------")
            add_member2 = add_conticue.add_member(member2[0], member2[1], mail=member2[3])

        with allure.step("8、点击页面下方的保存按钮；"):
            add_save = add_member2.click_save_button(2)

        with allure.step("9、断言页面提示【保存成功】；"):
            assert self.login.get_attribute(By.ID, "js_tips") == "保存成功"

        with allure.step("10、断言返回通讯录页面；"):
            assert add_save.get_page_title_text() == "Test"

        # with allure.step("11、判断添加的成员1，成员2信息在通讯录列表中。"):
        #     # todo 编写get_members
        #     assert member1[0] in add_save.get_members()
        #     assert member2[1] in add_save.get_members()
        # 为执行下一条案例等待页面刷新
        sleep(1)
        self.login.logging("-------------------------------- test_add_member_scene 结束 --------------------------------")

    @allure.story("添加成员")
    @allure.title("入口校验-从首页入口添加成员")
    def test_add_member_from_index(self, member_data):
        self.login.logging("------------------------------ test_add_member_from_index 开始------------------------------")
        member = member_data
        self.login.logging(f"--------member:{member[0], member[1], member[2]}--------")
        self.login.switch_index().click_add_member_button().\
            add_member(member[0], member[1], member[2]).click_save_button()
        self.login.logging("------------------------------ test_add_member_from_index 结束------------------------------")

    # todo 优化：需先获取页面页码，页码=循环全选删除次数，最后断言成员全部删除
    # @allure.story("成员管理-业务场景案例")
    # @allure.title("全部删除成员（全选-删除-确认）")
    def _test_clear_users(self):
        self.login.switch_index().click_contact_button().click_check_box().click_delete_button()
        # 获取成员列表
        # 断言成员列表仅包含创建人
        # assert
