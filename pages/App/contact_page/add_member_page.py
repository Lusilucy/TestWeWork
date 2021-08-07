# 添加成员页面
from pages.App.app import App


class AddMember(App):
    def click_manual_add(self):
        """
        点击手动输入添加成员
        :return: 编辑成员信息页面
        """
        self.find_xtext_click("手动输入添加")
        from pages.App.contact_page.edit_member_page import EditMember
        return EditMember(self.driver)

    # 微信邀请同事
    def click_wx_invate(self):
        pass

    # 从微信/手机通讯录中添加
    def click_wx_contact_add(self):
        pass
