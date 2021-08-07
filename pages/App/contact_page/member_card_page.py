from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException

from pages.App.app import App


class MemberCard(App):

    def click_edit_member(self):
        self.wait_visibility(MobileBy.XPATH, "//*[@text-xmind-csv='发消息']")
        try:
            self.driver.implicitly_wait(0)
            if self.find(MobileBy.XPATH, "//*[@text-xmind-csv='语音通话']"):
                self.driver.implicitly_wait(10)
                # 点击右上角按钮
                self.find_and_click(MobileBy.ID, 'com.tencent.wework:id/h8g')
                # 点击编辑成员按钮
                self.wait_presence(MobileBy.XPATH, '//*[@text-xmind-csv="编辑成员"]')
                self.find_and_click(MobileBy.XPATH, '//*[@text-xmind-csv="编辑成员"]')
                from pages.App.contact_page.update_member_page import UpdateMember
                return UpdateMember(self.driver)
        # 增加谨防点进创建人不可删除导致宕机的处理
        except NoSuchElementException:
            print('⚠️⚠️️点进了创建人名片，返回通讯录重新选择人员❗️')
            self.driver.implicitly_wait(10)
            self.back_contact().click_member_card()

    def back_contact(self):
        self.find_and_click(MobileBy.ID, 'com.tencent.wework:id/h86')
        from pages.App.contact_page.contact_page import Contact
        return Contact(self.driver)

    def send_message(self):
        pass
