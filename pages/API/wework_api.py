# WeWork公共方法（串联业务流程）
from pages.API.api import API


class WeWork(API):
    _url = "https://qyapi.weixin.qq.com/cgi-bin"

    def __init__(self, ID, SECRET, driver=None):
        super().__init__(driver)

        # 继承WeWork,初始化即获取token值
        self.token = self.get_access_token(ID, SECRET)

    def get_access_token(self, ID, SECRET):
        """
        获取token
        :param ID: 公司ID
        :param SECRET: 功能密钥
        :return: access_token值
        """
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={ID}&corpsecret={SECRET}"
        r = self.request("get", url)
        token = r.json()["access_token"]
        return token
