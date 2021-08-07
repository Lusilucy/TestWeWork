from selenium.webdriver.common.by import By

from pages.Web.contact_page.add_member import AddMember
from pages.Web.web import Web


class ChooseDepartments(Web):
    def choose_department(self, n):
        """

        :param n: 选择第几个部门
        :return: 停留当前页面
        """
        # todo 类比app进行优化
        # todo 选择部门js渲染，点击折页按钮时会奇怪刷新，可能刷新后定位不到元素，需寻求解决方法
        # 选择点击第几个部门元素（定位到的第4个元素开始是部门元素）
        self.finds_and_click_which(By.CSS_SELECTOR, ".jstree-anchor", n+3)
        return self

    def click_submit_button(self):
        self.find_and_click(By.CSS_SELECTOR, ".js_submit")
        return AddMember(self.driver)

    def click_cancel_button(self):
        self.find_and_click(By.CSS_SELECTOR, ".js_cancel")
        return AddMember(self.driver)
