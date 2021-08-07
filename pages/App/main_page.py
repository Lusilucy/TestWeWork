from pages.App.app import App
from utils.utils import Utils


class MainPage(App):
    eles = Utils.get_data("../../datas/conf_data/eles_data.yaml")['App']['main']

    def click_contact(self):
        """
        点击通讯录按钮
        :return: 通讯录页面
        """
        self.waits(*self.x_ele(self.eles['contact']))
        self.find_xtext_click("通讯录")
        from pages.App.contact_page.contact_page import Contact
        return Contact(self.driver)

    def click_workbench(self):
        """
        点击工作台页面
        :return: 工作台页面
        """
        self.find_xtext_click("工作台")
        from pages.App.workbench_page.workbench_page import WorkBench
        return WorkBench(self.driver)
