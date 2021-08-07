from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from pages.App.contact_page.add_member_page import AddMember
from pages.App.app import App
from utils.utils import Utils


# 手动输入添加成员页面
class EditMember(App):
    eles = Utils.get_data("../../datas/conf_data/eles_data.yaml")['App']['contact']['edit_member']

    def click_back_button(self):
        """
        点击页面返回按钮
        :return: 添加成员页面
        """
        self.find_and_click(*self.x_ele(self.eles['back']))
        return AddMember(self.driver)

    def click_change_edit(self):
        """
        点击切换输入方式按钮
        :return: 当前页面
        """
        # 点击切换页面按钮
        self.find_and_click(*self.x_ele(self.eles['change_edit']))
        # 等待页面加载
        self.wait_for_clickble(*self.x_ele(self.eles['name']))
        return self

    def choose_edit(self, which):
        """
        自主选择输入方式
        :param which: 输入方式
        :return: 当前页面
        """
        # 判断是否需要点击切换输入方式按钮
        if self.get_attribute(*self.x_ele(self.eles['change_edit']), 'text-xmind-csv') == which:
            self.click_change_edit()

        return self

    def edit_member_quick(self, name=None, mobile=None, area_code=None, invite=True):
        """
        快速输入成员信息
        :param name: 成员姓名
        :param mobile: 成员手机号
        :param area_code: 区码
        :param invite: 保存后自动发送邀请通知,True:点击复选框；False:不点击复选框；默认True
        :return: 当前页面
        """
        # 等待页面元素加载
        self.wait_for_clickble(*self.x_ele(self.eles['name']))
        # 如果数据传值，调用方法进行传值
        datas = {'name': name, 'area_code': area_code, 'mobile': mobile}
        for i in datas:
            if datas[i] is not None:
                self.find_and_sendkeys(*self.x_ele(self.eles[f'{i}']), datas[i])
        if invite is True:
            self.find_xtext_click("保存后自动发送邀请通知")
        return self

    def click_save_button(self):
        """
        点击页面保存按钮
        :return: 添加成员页面
        """
        self.find_xtext_click("保存")
        return AddMember(self.driver)

    def click_save_continue_button(self):
        """
        点击保存并继续添加按钮
        :return: 当前页面
        """
        self.find_xtext_click("保存并继续添加")
        return self

    def edit_member_full(
            self, name=None, mobile=None, email=None, area_code=None, userid=None, alias=None, gender=1,
            phone=None, address=None, positon=None, department=None, test_department=False,
            main_derparment=True, identity=False, other_position=None, invite=False, m=5
    ):
        """
        完整输入成员信息
        :param name: 姓名（必填）
        :param mobile: 手机号（与email不能同时为空）
        :param email: 邮箱（与mobile不能同时为空）
        :param area_code: 区号--None(默认):不修改区号;int:暂时写死为+355，后续可按照department进行优化
        :param userid: 帐号
        :param alias: 别名
        :param gender: 性别--1(默认):男；2:女
        :param phone: 座机
        :param address: 选填地址--None(默认):不填地址；str:选填地址
        :param positon: 职位
        :param department: 选填部门--None(默认):不修改部门信息；str:归属部门
        :param test_department: 是否测试部门页面--True:测试；False(默认):不测
        :param main_derparment: True(默认):是主部门；False:非主部门
        :param identity: 身份--True:上级；False(默认):普通员工
        :param other_position: 对外职位
        :param invite: True:邀请加入；False(默认):不邀请加入
        :param m: 页面刷新时，循环查找元素m次
        :return: 当前页面
        """

        # 等待页面元素加载
        self.wait_for_clickble(*self.x_ele(self.eles['name']))

        # 页面输入框传值
        datas = {
            'name': name, 'mobile': mobile, 'userid': userid,
            'alias': alias, 'phone': phone, 'email': email, 'positon': positon
        }
        for i in datas:
            if datas[i] is not None:
                self.find_and_sendkeys(*self.x_ele(self.eles[f'{i}']), datas[i])

        if gender == 2:
            # 点击性别选项框
            self.find_and_click(*self.x_ele(self.eles['gender_choose']))
            # 选择性别女
            self.find_xtext_click("女")

        if area_code is not None:
            # 点击区码选项框
            self.find_and_click(*self.x_ele(self.eles['area_code']))
            # 点击+355区码（暂不做测试，写死，后续可对照department进行优化）
            self.find_xtext_click("+355")

        if address is not None:
            # 点击地址选项框
            self.find_and_click(*self.x_ele(self.eles['address']))

            # 页面刷新，循环点击输入框直至找到元素
            # todo 优化：封装方法--页面刷新，循环点击
            for i in range(m):
                try:
                    self.find_and_click(*self.x_ele(self.eles['address_input']))
                    break
                except StaleElementReferenceException as e:
                    self.logging(f"----------------StaleElementReferenceException{i}:{e}----------------")

            # 输入地址
            self.find_and_sendkeys(*self.x_ele(self.eles['address_input']), address)

            # 页面刷新，循环点击搜索内容
            for i in range(m):
                try:
                    self.find_xtext_click(address, 2)
                    break
                except IndexError as e:
                    self.logging(f"----------------IndexError{i}:{e}----------------")

            # 点击确定按钮
            self.find_xtext_click("确定")

        # 向下滑动页面
        self.swip_and_find("保存后自动发送邀请通知")

        if department is not None:
            # 点击设置部门，跳转选择部门页面
            self.find_xtext_click("设置部门")
            if test_department is True:
                # 测部门页面时，跳转到选择部门页面进行自主操作
                return ChooseDepartment(self.driver)
            else:
                # 实例化选择部门页面（不测选择部门页面时，该部分操作写死）
                choose_department = ChooseDepartment(self.driver)

                choose_department.click_select_button().select_department(department)

                self.waits(*self.x_ele(f"//*[@text-xmind-csv='{department}']"), n=2)

                self.find_xtext_click(department, 2)

                choose_department.click_confirm_button()

            if main_derparment is True:
                self.find_and_click(*self.x_ele(self.eles['main_department']))
                self.wait_for_clickble(*self.x_ele("//*[@text-xmind-csv='设置']"))
                self.find_xtext_click("设置")

                # todo 偶发：如果界面弹出保存本次编辑弹框，点击确定
                self.driver.implicitly_wait(0)
                try:
                    if self.find(*self.x_ele("//*[@text-xmind-csv='保存本次编辑']")):
                        self.find_and_click(*self.x_ele("//*[@text-xmind-csv='确定']"))
                except NoSuchElementException:
                    pass
                self.driver.implicitly_wait(10)

        if identity is True:
            # 点击身份选项框
            self.find_xtext_click("身份")
            # 选择上级
            self.find_xtext_click("上级")

        if other_position is not None:
            # 点击对外职务选项框
            self.find_xtext_click("对外职务")
            # 输入对外职务
            self.find_xtext_sendkeys("请输入对外职务", other_position)
            # 点击确定按钮
            self.find_xtext_click("确定")

        # 不发送邀请
        if invite is False:
            self.swip_and_find("保存后自动发送邀请通知").click()

        return self


class ChooseDepartment(App):
    eles_d = Utils.get_data("../../datas/conf_data/eles_data.yaml")['App']['contact']['edit_member']['department']

    def choose_department(self, department_name):
        """
        选择部门
        :param department_name: 部门名称
        :return:
        """
        self.driver.implicitly_wait(0)

        try:
            self.find_xtext_click(f"{department_name}")
            self.driver.implicitly_wait(10)

        except NoSuchElementException:
            self.find_and_click(*self.x_ele(self.eles_d['unfold']))
            self.choose_department(department_name)

    def cancel_department(self, cancel_department):
        """
        点击页面下标取消部门
        :param cancel_department: 取消部门名称
        :return: 当前页面
        """
        self.find_xtext_click(cancel_department)
        return self

    def click_confirm_button(self):
        """
        点击确定按钮
        :return: 完整输入编辑成员页面
        """
        self.find_xtext_click("确定", c=True)
        return EditMember(self.driver)

    def click_select_button(self):
        """
        点击搜索按钮
        :return: 搜索页面
        """
        self.find_and_click(*self.x_ele(self.eles_d['select']))
        return self

    def select_department(self, department):
        """
        输入待搜索部门
        :param department: 部门名称
        :return: 当前页面
        """
        self.find_and_sendkeys(*self.x_ele(self.eles_d['input']), department)
        return self

    def click_back_button(self):
        """
        点击页面返回按钮
        :return: 完整输入编辑成员页面
        """
        self.find_and_click(*self.x_ele(self.eles_d['back']))
        return EditMember(self.driver)
