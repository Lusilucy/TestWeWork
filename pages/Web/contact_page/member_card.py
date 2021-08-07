# todo 成员详情页面（待编写）
from pages.Web.web import Web
from pages.myerror import NotFoundError


class MemberCard(Web):
    def get_member_details(self, attribute):
        # todo 定位+attribute
        # 定义界面内可获取成员信息的属性包含的内容
        attributes = []
        # 将元素定位放进列表中，与成员信息属性列表一一对应
        eles = []
        # 找到属性，获取成员该属性信息
        if attribute in attributes:
            index = attributes.index(attribute)
            return self.find(*eles[index])
        else:
            # 输入属性不存在返回摆错
            raise NotFoundError("attribude can not found in pages! Please check your args!")

    # 点击返回按钮
    def click_return_button(self):
        # from pages.Web.contact_page.contact_page import ContactPage
        # return ContactPage(self.driver)
        pass

    # 点击编辑按钮
    def click_edit_button(self):
        pass
        # from pages.Web.contact_page.update_member import UpdateMember
        # return UpdateMember(self.driver)

    # 点击删除按钮
    def click_delete_button(self):
        pass

    # 点击禁用按钮
    def click_disable_button(self):
        pass
