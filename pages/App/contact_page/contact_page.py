from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from pages.App.app import App


class Contact(App):
    def click_add_member_card(self):
        """
        点击添加成员
        :return: 添加成员页面
        """
        self.swip_and_find("添加成员", n=10).click()
        from pages.App.contact_page.add_member_page import AddMember
        return AddMember(self.driver)

    # 点击成员，默认点击可见的除'创建人'外的第一个成员
    def click_member_card(self, name=None):
        self.select_member(name).click()
        from pages.App.contact_page.member_card_page import MemberCard
        return MemberCard(self.driver)

    # 点击部门
    def click_department_card(self):
        pass

    # 点击我的客户
    def click_my_customer_card(self):
        pass

    # 获取全部通讯录名单
    def get_contacts(self):
        contacts = []
        # 滑动回通讯录顶部
        self.scroll_to_top()

        # 定义方法：获取当前页面通讯录名单
        def get_member():
            i = 0
            while True:
                i += 1
                try:
                    if i == 5:
                        print('系统异常，多次刷新，请查看并手动调试！')
                        raise TimeoutException
                    eles = self.finds(
                        *self.x_ele('//*[@resource-id="com.tencent.wework:id/he1"]/android.widget.TextView'))
                    for e in eles:
                        contacts.append(e.get_attribute('text-xmind-csv'))
                    break
                except StaleElementReferenceException:
                    print(f'提示⚠️：get_member失败,通讯录页面刷新中')
                    continue

        self.swip_and_find("添加成员", get_member)
        print(f'当前页面成员名单为：{contacts}')
        return contacts
