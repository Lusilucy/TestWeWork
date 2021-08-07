# 通讯录主页面
from selenium.webdriver.common.by import By

from pages.Web.web import Web


# 通讯录页面
class ContactPage(Web):
    def click_add_member_button(self, n=2):
        """
        点击添加成员按钮
        :param n:1：页面上部按钮（默认）；2：页面下部按钮；0：部门无成员时页面中间的按钮
        :return: 添加成员功能
        """
        # 等待页面元素加载
        self.wait_for_clickble(By.CSS_SELECTOR, ".ww_operationBar .js_add_member")
        # 循环点击添加成员按钮
        self.wait_load_click(By.CSS_SELECTOR, ".js_add_member", By.ID, "username", n+1)
        from pages.Web.contact_page.add_member import AddMember
        return AddMember(self.driver)

    def click_check_box(self, n=1):
        """
        点击通讯录页面成员复选框
        :param n: 默认全选；1：全选；2：第一个成员；3：第二个成员，以此类推…-1：最后一个成员；-2：倒数第二个成员，以此类推…
        :return:停留当前页面
        """
        # 等待复选框可点击
        self.wait_for_clickble(By.CSS_SELECTOR, ".ww_checkbox")
        # 点击复选框
        self.finds_and_click_which(By.CSS_SELECTOR, ".ww_checkbox", n)
        return self

    def click_delete_button(self, n=1, submit=1):
        """
        点击删除按钮，并确认是否删除
        :param n: 默认点击页面上部按钮；1：上部按钮；2：下部按钮
        :param submit: 默认确认；1:确认；2:取消；其他：关闭
        :return: 停留当前页面
        """
        # 等待删除按钮可点击
        self.wait_for_clickble(By.CSS_SELECTOR, ".ww_operationBar .js_delete")
        # 点击删除按钮
        self.finds_and_click_which(By.CSS_SELECTOR, ".ww_operationBar .js_delete", n)
        # 等待删除确认页面元素可点击
        self.wait_for_clickble(By.CSS_SELECTOR, ".ww_dialog .ww_btn")
        if submit == 1:
            # 确认
            self.finds_and_click_which(By.CSS_SELECTOR, ".ww_dialog .ww_btn", 1)
        elif submit == 2:
            # 取消
            self.finds_and_click_which(By.CSS_SELECTOR, ".ww_dialog .ww_btn", 2)
        else:
            # 关闭
            self.find_and_click(By.CSS_SELECTOR, ".ww_dialog_close")

        return self

    # 点击翻页按钮
    def click_page(self):
        pass

    def get_members(self, p: int = None):
        """
        获取当前页面通讯录成员列表
        :param p: 查看第几页成员列表（默认不翻页）
        :return: 停留在当前页面
        """
        pass
        # return self

    # 点击成员信息
    def click_member_table(self):
        pass
        # from pages.Web.contact_page.member_card import MemberCard
        # return MemberCard(self.driver)

    # 获取页面标题名称
    def get_page_title_text(self):
        try:
            page_title_text = self.get_attribute(By.ID, "party_name")
            return page_title_text
        except Exception as e:
            self.logging(f"未获取到通讯录页标题信息，具体报错为：{e}")
            return e

    # todo DepartmentFrame优化：(1、放在此方法中是否方便调用；2、检查代码；
    #  3、页面元素可能全部在，但由于肉眼不可见，可能点击不生效导致点击后页面不刷新，导致未显示所选部门成员列表)
    class DepartmentFrame(Web):
        def choose_department(self, n):
            """
            选择展示的部门
            :param n: n=1,展示的第一个部门，n=2展示的第二个部门，以此类推
            :return:
            """
            self.logging("--------choose_department--------")
            while True:
                try:
                    # 找目标部门并点击
                    self.finds_and_click_which(By.CSS_SELECTOR, ".jstree-anchor", n)
                    return self
                except Exception as e:
                    self.logging(f"errormsg:{e}")
                    # 找展开列表按钮元素
                    eles = self.finds(By.CSS_SELECTOR, ".jstree-ocl")
                    for i in eles:
                        try:
                            i.click()
                        except Exception:
                            continue
