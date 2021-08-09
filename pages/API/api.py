# 封装接口测试独有方法，使架构更清晰
import requests

from pages.base import Base


class API(Base):
    Base.set_log("../../logs/apitest.log")

    def request(self, method, url, json=None):
        """
        封装requests.request方法
        :param method: 请求方法
        :param url: 请求URL
        :param json: post请求携带的json数据
        :return:response响应体
        """
        self.logging("---------------请求参数---------------")
        self.logging(f"method:{method},url:{url}")
        self.logging(f"data:{json}")
        r = requests.request(method, url, json=json)
        self.logging("---------------响应参数---------------")
        self.logging(f"response:{r.json()}")
        return r
