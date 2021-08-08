# 封装web公共方法
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base import Base
from pages.myerror import NotFoundError
from utils.utils import Utils


class Web(Base):
    Base.set_log("./logs/webtest.log")

    def __init__(self, driver: WebDriver = None):
        # todo 设置启用不同浏览器，测试兼容性
        # driver=None，创建driver
        if driver is None:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(5)
        # 复用driver
        else:
            self.driver = driver

    # 关闭浏览器
    def quit(self):
        self.driver.quit()

    def wait_load_click(self, by1, locator1, by2, locator2, n=None, a=10):
        """
        页面加载找到元素点击不生效（显示等待元素可点击由于页面刷新也不生效）时，暴力循环点击元素，直至新页面元素出现
        :param by1: 点击的元素定位方式
        :param locator1: 点击的元素定位符
        :param by2: 等待的元素定位方式
        :param locator2: 等待的元素定位符
        :param n: n=None:调用点击找到的第一个元素方法，n=int:调用点击找到的第几个元素方法
        :param a: 循环点击次数，默认10次
        :return:
        """
        self.logging("--------------------------wait_load_click--------------------------")
        self.driver.implicitly_wait(0)
        for i in range(a):
            try:
                if n is None:
                    self.find_and_click(by1, locator1)
                else:
                    self.finds_and_click_which(by1, locator1, n)

            except Exception as e:
                self.logging(f"--------------------------捕获异常{i}：{e}--------------------------")
                if i == a-1:
                    raise NotFoundError

            if len(self.finds(by2, locator2)) > 0:
                self.driver.implicitly_wait(5)
                break


# todo 思考：优化，cookies过期时，仅需人工扫码即可重新自动运行
# cookies过期时，调用方法复用浏览器重新获取cookies，存入文档中
class Cookies(Base):
    @classmethod
    def get_cookies(cls):
        """
        本地操作
        开启chrome应用debug模式 --remote-debugging-port=9222
        打开企业微信扫码登录界面，重新扫码登录
        存储登录cookies到TestWework/datas/conf_data/cokkies_web.yaml文件中
        :return: 返回本身
        """
        # 执行shell启动复用浏览器界面
        # cls.shell(cls, './launch_chrome.sh')
        # import os
        # os.system("./launch_chrome.sh")
        # todo 在pycharm中执行shell文件未在本地启动复用浏览器，在terminal中进入python执行shell文件可用（是pycharm问题？）

        # 复用浏览器
        cls.logging(Base(), "----------------复用浏览器更新cookies----------------")
        opt = webdriver.ChromeOptions()
        opt.debugger_address = "127.0.0.1:9222"
        driver = webdriver.Chrome(options=opt)
        driver.implicitly_wait(5)
        # 打开微信首页
        driver.get("https://work.weixin.qq.com/wework_admin/frame#index")
        # 等待30s手工扫码
        Web(driver).waits(By.CSS_SELECTOR, ".login_head_title", 30, False)
        # 获取cookies
        cookies = driver.get_cookies()
        # 存入yaml文件保存
        Utils.dump_data(cookies, "../../datas/conf_data/cookies_web.yaml")
        driver.quit()
        cls.logging(Base(), "----------------更新cookies完成----------------")
        # todo 1、未知原因引起长时间死等大概30-60s；2、driver.quit()不生效（复用浏览器无法quit()）

