from selenium.webdriver.common.by import By

from pages.Web.web import Web, Cookies
from utils.utils import Utils


# 登录页
class LoginPage(Web):
    def __init__(self, driver=None):
        super().__init__(driver)
        # 打开企业微信扫码登录界面
        self.driver.get("https://work.weixin.qq.com/wework_admin/loginpage_wx")
        # 传入cookies
        try:
            cookies = Utils.get_data("../../datas/conf_data/cookies_web.yaml")
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except FileNotFoundError:
            self.driver.quit()
            Cookies.get_cookies()

    def switch_index(self):
        """
        跳转首页页面
        :return: 企业微信首页页面
        """
        # 进入企业微信首页
        self.driver.get("https://work.weixin.qq.com/wework_admin/frame#index")
        # 检查是否登录成功
        if self.check_login() is True:
            from pages.Web.index_page.index_page import IndexPage
            return IndexPage(self.driver)

    def switch_contact(self):
        """
        跳转通讯录页面
        :return: 企业微信通讯录页面
        """
        self.driver.get("https://work.weixin.qq.com/wework_admin/frame#contacts")
        from pages.Web.contact_page.contact_page import ContactPage
        return ContactPage(self.driver)

    # 跳转应用管理页面
    def switch_apps(self):
        self.driver.get("https://work.weixin.qq.com/wework_admin/frame#apps")
        self.check_login()

    # 跳转客户联系页面
    def switch_customer(self):
        self.driver.get("https://work.weixin.qq.com/wework_admin/frame#customer/analysis")
        self.check_login()

    # 跳转管理工具页面
    def switch_managetools(self):
        self.driver.get("https://work.weixin.qq.com/wework_admin/frame#manageTools")
        self.check_login()

    # 跳转我的企业页面
    def switch_profile(self):
        self.driver.get("https://work.weixin.qq.com/wework_admin/frame#profile")
        self.check_login()

    # 检查登录是否成功，若不成功，cookies过期，重新获取cookies
    def check_login(self):
        self.driver.implicitly_wait(0)

        try:
            if self.get_attribute(By.ID, "js_tips") == "登录态过期，请重新登录":
                self.logging("-------------cookies过期，请检查！-------------")
                self.logging("-------------cookies过期，请启动shell脚本复用浏览器，并再次运行2次！（1、扫码登录，更新cookies；2、重新运行案例）-------------")
                self.driver.quit()
                Cookies.get_cookies()
                return False
        except Exception as e:
            self.logging(f"-------------检查登录Exception:{e}-------------")
        self.driver.implicitly_wait(5)
        return True
