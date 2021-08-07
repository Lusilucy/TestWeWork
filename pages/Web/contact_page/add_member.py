from selenium.webdriver.common.by import By

from pages.Web.contact_page.contact_page import ContactPage
from pages.Web.web import Web


class AddMember(Web):
    # todo edit_user 待完善所有元素定位（对照app完整输入方法进行封装）
    def add_member(self, username=None, acctid=None, phone=None, mail=None, department: int = None, n=5):
        """
        编辑成员信息
        :param username:姓名（必填项）
        :param acctid:帐号（必填项）
        :param phone:手机（与mail不能同时为空）
        :param mail:邮箱（与phone不能同时为空）
        :param department:部门（选填项，不填代表使用默认部门，不进行编辑，传任意数字，进入修改部门操作）
        :param n:等待页面加载刷新次数，默认5次
        :return:停留当前页面
        """
        # 等待姓名输入框可被点击
        for i in range(n):
            self.find_and_click(By.CSS_SELECTOR, ".member_edit_cover")
            self.find_and_click(By.ID, "username")
            a = self.get_attribute(By.ID, "username", "aria-invalid")
            if a == "true":
                break

        # 页面各输入框元素定位
        e_username = (By.ID, "username")
        e_acctid = (By.ID, "memberAdd_acctid")
        e_phone = (By.ID, "memberAdd_phone")
        e_mail = (By.ID, "memberAdd_mail")
        e_department = (By.CSS_SELECTOR, ".js_show_party_selector")
        # 如果数据传值，调用方法进行传值
        datas = [username, acctid, phone, mail]
        eles = [e_username, e_acctid, e_phone, e_mail]
        for i in datas:
            if i is not None:
                n = datas.index(i)
                self.find_and_sendkeys(*eles[n], i)

        # todo 部门浮窗逻辑优化（类比app）
        # 当部门传值时，代表修改部门数据
        if department is not None:
            # 点击修改部门，弹出部门修改浮窗，跳转选择部门浮窗
            self.find_and_click(*e_department)
            from pages.Web.contact_page.choose_department import ChooseDepartments
            return ChooseDepartments(self.driver)

        return self

    def click_save_button(self, n=1):
        """
        点击页面保存按钮
        :param n: 选择点击哪一个保存按钮，默认点击第一个
        :return: 返回通讯录页面
        """
        self.finds_and_click_which(By.CSS_SELECTOR, ".js_btn_save", n)
        return ContactPage(self.driver)

    def click_save_and_continue_button(self, n: int = 1):
        """
        点击页面保存并继续按钮
        :param n: 选择点击哪一个保存并继续按钮，默认点击第一个
        :return: 返回当前添加成员功能页面
        """
        self.finds_and_click_which(By.CSS_SELECTOR, ".js_btn_continue", n)
        return self

    def click_cancel_button(self, n: int = 1):
        """
        点击页面取消按钮
        :param n: 选择点击哪一个取消按钮，默认点击第一个
        :return: 返回当前添加成员功能页面
        """
        self.finds_and_click_which(By.CSS_SELECTOR, ".js_btn_cancel", n)
        return ContactPage(self.driver)

    # 获取页面标题名称
    def get_page_title_text(self):
        try:
            page_title_text = self.get_attribute(By.CSS_SELECTOR, ".ww_commonCntHead_title_inner_text", "textContent",2)
            return page_title_text
        except Exception as e:
            self.logging(f"未获取到添加成员页标题信息，具体报错为：{e}")
            return e
