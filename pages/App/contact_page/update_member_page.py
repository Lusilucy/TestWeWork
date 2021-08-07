from appium.webdriver.common.mobileby import MobileBy

from pages.App.app import App


class UpdateMember(App):
    def __init__(self, driver):
        super().__init__(driver)
        self.member_name = self.find(
            MobileBy.XPATH, "//*[contains(@text-xmind-csv,'姓名')]/../*[@resource-id='com.tencent.wework:id/ays']"
        ).get_attribute('text-xmind-csv')
        self.member_ID = self.find(
            MobileBy.XPATH, "//*[contains(@text-xmind-csv,'帐号')]/../*[@resource-id='com.tencent.wework:id/ays']"
        ).get_attribute('text-xmind-csv')

    def delete_member(self):
        # 滑动页面找到并点击删除成员按钮
        self.swip_and_find('删除成员').click()
        # 删除确认
        self.find_and_click(MobileBy.XPATH, "//*[@text-xmind-csv='确定']")
        # 显示等待页面加载
        self.wait_contact_load()
        from pages.App.contact_page.contact_page import Contact
        return Contact(self.driver)
