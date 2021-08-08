# 封装app独有方法
from datetime import datetime

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException

from pages.base import Base
from pages.myerror import NoneMemberException


class App(Base):
    # 日志存放路径
    Base.set_log("./logs/apptest.log")

    def start(self):
        """
        启动app
        :return: 启动页面
        """
        self.logging("----------------启动app----------------")
        if self.driver is None:
            self.logging("----------------创建driver----------------")
            caps = {}
            caps["platformName"] = "android"
            caps["deviceName"] = "Rose"
            caps["appPackage"] = "com.tencent.wework"
            caps["appActivity"] = ".launch.LaunchSplashActivity"
            caps["noReset"] = True
            # caps["dontStopAppOnReset"] = True
            self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
            self.driver.implicitly_wait(10)
        else:
            self.logging("----------------复用driver----------------")
            self.driver.launch_app()
        return self

    def restart(self):
        """
        重启app（暖启动）
        :return: 启动页面
        """
        self.logging("----------------重启app----------------")
        self.driver.close()
        self.driver.launch_app()
        return self

    def back(self, n=1):
        """
        操作手机返回
        :param n: 返回次数;默认值为1
        :return: None
        """
        self.logging(f"----------------操作{n}次返回键----------------")
        for i in range(n):
            self.driver.back()

    def stop(self):
        """
        杀掉app
        :return: None
        """
        self.logging("----------------杀掉app----------------")
        self.driver.quit()

    def goto_main(self):
        """
        进入app主页
        :return: app主页
        """
        self.logging("----------------进入主页----------------")
        from pages.App.main_page import MainPage
        return MainPage(self.driver)

    def x_ele(self, location):
        """
        通过xpath定位的元素
        :param location: "定位"
        :return: (MobileBy.XPATH,"定位")
        """
        self.logging(f"----------------MobileBy.XPATH,location:{location}----------------")
        return (MobileBy.XPATH, f"{location}")

    def find_xtext_ele(self, text):
        """
        封装find_by_xpath方法（APP）
        :param text: 所定位元素的text属性
        :return: 定位的元素
        """
        self.logging(f"----------------find_by_xpath:{text}----------------")
        return self.find(MobileBy.XPATH, f"//*[@text='{text}']")

    def finds_xtext_ele(self, text):
        """
        封装finds_by_xpath方法（APP）
        :param text: 所定位元素的text属性
        :return: 包含text属性的元素列表
        """
        self.logging(f"----------------find_by_xpath:{text}----------------")
        return self.finds(MobileBy.XPATH, f"//*[contains(@text,'{text}')]")

    def find_xc_text_ele(self, text):
        """
        封装find_by_xpath方法（APP）
        :param text: 所定位元素的text属性
        :return: 定位的元素
        """
        self.logging(f"----------------find_by_xpath_contains:{text}----------------")
        return self.find(MobileBy.XPATH, f"//*[contains(@text,'{text}')]")

    def find_xtext_click(self, text, n=1, c=None):
        """
        封装find_by_xpath并点击方法
        :param text: 所定位元素的text属性
        :param n: 默认n=1;选取定位到的第n个元素
        :param c: 默认c=None;c=None:text属性=text值;c!=None:text属性包含text内容
        :return: 点击元素
        """
        self.logging("----------------find_by_xpath_and_click----------------")

        if c is not None:
            return self.find_xc_text_ele(text).click()
        elif n != 1:
            return self.finds_xtext_ele(text)[n-1].click()
        else:
            return self.find_xtext_ele(text).click()

    def find_xtext_sendkeys(self, text, value, c=None):
        """
        封装find_by_xpath并上送数据方法
        :param text: 所定位元素的text属性
        :param value: 上送数据value
        :param c: 默认c=None;c=None:text属性=text值;c!=None:text属性包含text内容
        :return: 找到元素并上送value
        """
        self.logging(f"----------------find_by_xpath_and_sendkeys:{value}----------------")

        if c is not None:
            return self.find_xtext_ele(text).send_keys(value)
        else:
            return self.find_xc_text_ele(text).send_keys(value)

    def check_toast(self):
        """
        获取toast提示信息
        :return: toast的text属性值
        """
        return self.get_attribute(*self.x_ele("//*[@class='android.widget.Toast']"), 'text')

    def swip_and_find(self, text, fun=None, n=5):
        """
        滑动页面(并执行函数)查找元素
        :param text: 所查找元素的text属性
        :param fun: 滑动并执行函数，默认值为None
        :param n: 滑动次数，默认5次
        :return: 找到的元素
        """
        self.logging(f"----------------swip_and_find:{text} & carry_out: {fun}----------------")
        self.logging(f"swip_start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")

        window = self.driver.get_window_rect()
        height = window['height']
        width = window['width']
        start_x = width / 2
        start_y = height * 0.8
        end_x = start_x
        end_y = height * 0.2
        self.driver.implicitly_wait(0)

        # 定义一个函数：判断是否传入函数，若传入函数，执行参数，若未传入参数，跳过此步
        def have_fun(f):
            if f is None:
                pass
            else:
                f()

        for i in range(n):
            try:
                ele = self.driver.find_element(MobileBy.XPATH, f"//*[@text='{text}']")
                have_fun(fun)
                self.driver.implicitly_wait(10)
                return ele
            except NoSuchElementException as e:
                self.logging(f"----------------NoSuchElementException{i}:{e}----------------")
                have_fun(fun)
                self.driver.swipe(start_x, start_y, end_x, end_y, 1000)

    def scroll_findtext_click(self, text):
        """
        滑动查找页面元素
        :param text: 所查找元素的text属性
        :return: 找到的元素
        """
        self.logging(f"----------------scoll_and_find_by_text:{text}:_and_click----------------")
        return self.driver.find_element(MobileBy.ANDROID_UIAUTOMATOR,
                                        f'new UiScrollable(new UiSelector().scrollable(true).instance(0)).'
                                        f'scrollIntoView(new UiSelector().text("{text}").instance(0));').click()

    # 选择当前页面成员元素
    def select_member(self, name=None, n=1):
        m = 0
        # 选择当前页面除'创建人'外的成员元素（n=1默认第一个成员，n=0为我的客户）
        while True:
            m += 1
            ele1 = self.find(MobileBy.XPATH, f'//*[@resource-id="com.tencent.wework:id/dyi"][{n + 1}]'
                                             f'//*[@resource-id="com.tencent.wework:id/he1"]/android.widget.TextView')
            ele2 = self.find(MobileBy.XPATH, f'//*[@resource-id="com.tencent.wework:id/dyi"][{n + 2}]'
                                             f'//*[@resource-id="com.tencent.wework:id/he1"]/android.widget.TextView')

            try:
                # 避免找不到创建人时强制隐式等待，取消隐式等待
                self.driver.implicitly_wait(0)
                ele_original1 = self.find(
                    MobileBy.XPATH, "//*[@resource-id='com.tencent.wework:id/b4j']/.."
                                    "//*[@resource-id='com.tencent.wework:id/he1']/android.widget.TextView")
                if ele1.get_attribute('text') == ele_original1.get_attribute('text'):
                    print('debug6')
                    element = ele2
                    if element.get_attribute('text') == '添加成员':
                        print('提示⚠️：当前页面无可删除成员，请确认')
                        raise NoneMemberException
                else:
                    print('debug7')
                    element = ele1
            except NoSuchElementException:
                print('⚠️当前界面无创建人')
                element = ele1
            if m == 8:
                # 循环8次页面仍有上次删除的人员名字（1.页面一直未刷新 or 2.页面早已刷新完毕 or 3.存在重名情况）
                # 取最后一次element取值，跳出循环结束
                # 等待页面未刷新则系统自动报错，重名或页面早已刷新完毕则继续删除成员
                print('⚠️当前页面已刷新或存在重名成员,请关注删除情况')
                break

            elif name is not None:
                if element.get_attribute('text') != name:
                    print('debug8')
                    # 连续第2次删除成员时，检查页面预查询到的成员与待删除成员是否一致，不一致，结束并删除
                    try:
                        # 增加判断解决❓1⃣️ ，已复现情况，起到解决作用👍
                        ele_original2 = self.find(
                            MobileBy.XPATH, "//*[@resource-id='com.tencent.wework:id/b4j']/.."
                                            "//*[@resource-id='com.tencent.wework:id/he1']/android.widget.TextView")
                        if element.get_attribute('text') == ele_original2.get_attribute('text'):
                            print('debug1')  # 为找到偶发点进创建人bug而打的断点
                            continue
                    except NoSuchElementException:
                        print('debug2')
                        break
                    print('debug3')
                    break
                else:
                    # 一致,可能为返回通讯录过快，通讯录未刷新已删除成员仍存在的原因，因此循环查询8次
                    print('debug4')
                    continue
            else:
                # 第一次删除成员时，name送空，不需要等待刷新
                print('debug5')
                break
        # 恢复隐式等待
        self.driver.implicitly_wait(10)
        return element

    # 显示等待通讯录页面加载
    def wait_contact_load(self, sec=10):
        self.logging('wait_contact_load')
        self.wait_visibility(MobileBy.XPATH, '//*[@resource-id="com.tencent.wework:id/he1"]', sec)

    # 滑动回页面顶部（默认通讯录页面顶部）
    def scroll_to_top(self, text="我的客户"):
        self.logging(f"scroll_to: {text}")
        self.logging(f"scroll_start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        self.find(
            MobileBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true).'
            f'instance(0)).scrollIntoView(new UiSelector().text("{text}").instance(0))')
        self.logging(f"scroll_end: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
