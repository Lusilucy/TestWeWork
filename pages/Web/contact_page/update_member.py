from pages.Web.contact_page.contact_page import ContactPage
from pages.Web.web import Web


# 单个成员编辑修改页面
class UpdateMember(Web):
    def update_member(self):
        return self

    def click_save_button(self):
        return ContactPage(self.driver)

    def click_cancel_button(self):
        return self
