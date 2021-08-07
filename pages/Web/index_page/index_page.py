# 首页
from selenium.webdriver.common.by import By

from pages.Web.web import Web


class IndexPage(Web):
    def click_add_member_button(self):
        """
        点击添加成员按钮
        :return: 跳转到通讯录-添加成员功能页面
        """
        self.find_and_click(By.CSS_SELECTOR, ".js_service_list a:nth-child(1)")
        from pages.Web.contact_page.add_member import AddMember
        return AddMember(self.driver)

    def click_contact_button(self):
        """
        点击切换到通讯录页面
        :return: 跳转到通讯录页面
        """
        self.find_and_click(By.ID, "menu_contacts")
        from pages.Web.contact_page.contact_page import ContactPage
        return ContactPage(self.driver)

