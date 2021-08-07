import os
from datetime import datetime

from jsonpath import jsonpath
import logging

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Base:
    # 封装公共方法，使page中不需要引入其他包，直接调用公共方法

    def __init__(self, driver=None):
        self.driver = driver

    @classmethod
    def set_log(self, file_path):
        """
        封装设置日志级别方法
        :param file_path: 设置日志存放路径
        """
        fileHandler = logging.FileHandler(filename=file_path, encoding="utf-8")
        logging.getLogger().setLevel(0)
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(module)s:%(lineno)d %(message)s')
        fileHandler.setFormatter(formatter)
        logging.getLogger().addHandler(fileHandler)

    # 封装日志打印方法
    def logging(self, msg):
        return logging.info(msg)

    def jpath(self, obj, expr):
        """
        封装jsonpath方法
        :param obj: json串
        :param expr: 定位符
        :return: 符合定位的数据的列表
        """
        return jsonpath(obj, expr)

    def shell(self, file_path):
        """
        封装执行shell脚本命令
        :param file_path: 读取.sh文件路径
        :return: 执行shell
        """
        return os.system(file_path)

    def find(self, by, locator):
        """
        封装查找元素方法
        :param by: 定位方式
        :param locator: 定位符
        :return: 找到元素 or 未找到元素返回报错
        """
        self.logging("----------------find_start----------------")
        self.logging(f"--------by:{by};locator:{locator}--------")
        ele = self.driver.find_element(by, locator)
        self.logging("----------------find_end----------------")
        return ele

    def find_and_click(self, by, locator):
        """
        封装查找并点击元素方法
        :param by: 定位方式
        :param locator: 定位符
        :return: 点击元素 or 未找到元素返回报错
        """
        self.logging("----------------find_and_click----------------")
        return self.find(by, locator).click()

    def find_and_sendkeys(self, by, locator, value):
        """
        封装查找元素并传值方法
        :param by: 定位方式
        :param locator: 定位符
        :param value: 传值
        :return: 传值 or 未找到元素报错
        """
        self.logging(f"----------------find_and_sendkeys:{value}----------------")
        return self.find(by, locator).send_keys(value)

    def finds(self, by, locator):
        """
        封装查找多个元素方法
        :param by: 定位方式
        :param locator: 定位符
        :return: 找到的元素定位列表
        """
        self.logging("----------------finds_start----------------")
        self.logging(f"--------by:{by};locator:{locator}--------")
        eles = self.driver.find_elements(by, locator)
        self.logging("----------------finds_end----------------")
        return eles

    def finds_and_click_which(self, by, locator, n):
        """
        封装找到多个元素，点击其中某个元素
        :param by: 定位方式
        :param locator: 定位符
        :param n: 第n个元素
        :return: 点击元素 or 未找到元素返回报错
        """
        self.logging("----------------finds_and_click_which----------------")
        eles = self.finds(by, locator)
        self.logging(f"--------点击页面上该定位符找到的第{n}个元素--------")
        return eles[n-1].click()

    def get_attribute(self, by, locator, attribute="textContent", n: int = None):
        """
        获取元素text内容
        :param by: 定位方式
        :param locator:定位符
        :param attribute:属性，默认获取textContent属性值
        :param n:定位到多个元素，选择第几个元素获取属性值
        :return: 获取元素的的text或其他属性值
        """
        if n is None:
            self.logging("----------------find_and_get_text----------------")
            a = self.find(by, locator).get_attribute(attribute)
        else:
            self.logging("----------------finds_and_get_text----------------")
            a = self.finds(by, locator)[n - 1].get_attribute(attribute)
        self.logging(f"--------获取到的{attribute}的值为:{a}--------")
        return a

    def waits(self, by, locator, sec=10, appear=True, n: int = 1):
        """
        显示等待直至找到页面元素
        :param by: 定位方式
        :param locator: 定位符
        :param sec: 等待时间，默认10s
        :param appear:True:等待直至元素出现，False:等待直至元素消失
        :param n: 元素在界面出现的次数，默认有1个即可
        :return: True or Timeout
        """
        self.logging("----------------waits----------------")
        self.logging(f"--------by:{by},locator:{locator},sec:{sec},appear:{appear}, n:{n}--------")
        if appear is True:
            WebDriverWait(self.driver, sec).until(lambda x: len(self.finds(by, locator)) >= n)
        else:
            WebDriverWait(self.driver, sec).until_not(lambda x: len(self.finds(by, locator)) >= n)

    def wait_for_clickble(self, by, locator, sec=10):
        """
        显示等待直至页面元素可被点击
        :param by: 定位方式
        :param locator: 定位符
        :param sec: 等待时间，默认10s
        :return: True or Timeout
        """
        self.logging("----------------wait_for_clickble----------------")
        self.logging(f"--------by:{by},locator:{locator},sec:{sec}--------")
        return WebDriverWait(self.driver, sec).until(expected_conditions.element_to_be_clickable((by, locator)))

    # 显示等待元素可见
    def wait_visibility(self, by, locator, sec=10):
        self.logging(f"wait_visibility_by: {by}, {locator}")
        self.logging(f"wait_visibility_start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        WebDriverWait(self.driver, sec).until(expected_conditions.visibility_of_element_located((by, locator)))
        self.logging(f"wait_visibility_end: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")

    # 显示等待元素存在（存在不一定可见）
    def wait_presence(self, by, locator, sec=10):
        self.logging(f"wait_presence_by: {by}, {locator}")
        self.logging(f"wait_presence_start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        WebDriverWait(self.driver, sec).until(expected_conditions.presence_of_element_located((by, locator)))
        self.logging(f"wait_presence_end: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
