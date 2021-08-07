# 成员接口
from time import sleep

from pages.API.wework_api import WeWork


class User(WeWork):
    def create_user(self, data):
        """
        创建成员
        :param data:详见WeWork/datas/create_user_demo.json
        :return:errcode:0,errmsg:created
        """
        url = f"{self._url}/user/create?access_token={self.token}&debug=1"
        r = self.request("post", url, data)
        return r.json()

    def get_user(self, USERID):
        """
        读取成员信息
        :param USERID:成员ID
        :return:errcode:0,errmsg:ok,成员详细信息
        """
        url = f"{self._url}/user/get?access_token={self.token}&userid={USERID}&debug=1"
        r = self.request("get", url)
        return r.json()

    def updata_user(self, data):
        """
        更新成员信息
        :param data:详见WeWork/datas/update_user_demo.json
        :return:errcode:0,errmsg:updated
        """
        url = f"{self._url}/user/update?access_token={self.token}&debug=1"
        r = self.request("post", url, data)
        return r.json()

    def delete_user(self, USERID):
        """
        删除成员
        :param USERID: 成员ID
        :return: errcode:0,errmsg:deleted
        """
        url = f"{self._url}/user/delete?access_token={self.token}&userid={USERID}&debug=1"
        r = self.request("get", url)
        return r.json()

    def batch_delete_users(self, data):
        """
        批量删除成员
        :param data: userlist,详见WeWork/datas/batch_delete_users_demo.json
        :return: errcode:0,errmsg:deleted
        """
        url = f"{self._url}/user/batchdelete?access_token={self.token}&debug=1"
        r = self.request("post", url, data)
        return r.json()

    def get_simple_list(self, ID):
        """
        获取部门成员简单信息
        :param ID: 部门ID
        :return: errcode:0,errmsg:ok,userlist:[]
        """
        url = f"{self._url}/user/simplelist?access_token={self.token}&department_id={ID}&debug=1"
        r = self.request("get", url)
        return r.json()

    # 清理测试环境,删除部门下所有成员
    def clear_user_datas(self, department_id):
        # 获取部门成员ID列表
        r = self.get_simple_list(department_id)
        ids = self.jpath(r, "$..userid")
        print(ids)

        # 如果列表不为空，且成员不为创建人，循环删除成员
        if ids is not False:
            for i in ids:
                # 删除创建人不会成功，不需要规避
                if i != "LuSi":
                    r = self.delete_user(i)
                    print(r)
                    # 规避接口调用频率限制
                    sleep(2)

    def get_list(self, DEPARTMENT_ID):
        """
        获取部门成员详情
        :param DEPARTMENT_ID:部门ID
        :return: errcode:0,errmsg:ok,userlist:[]
        """
        url = f"{self._url}/user/list?access_token={self.token}&department_id={DEPARTMENT_ID}&debug=1"
        r = self.request("get", url)
        return r.json()

    # userid转openid
    def convert_to_openid(self, data):
        url = f"{self._url}/user/convert_to_openid?access_token={self.token}&debug=1"
        r = self.request("post", url, data)
        return r.json()

    # openid转userid
    def convert_to_userid(self, data):
        url = f"{self._url}/user/convert_to_userid?access_token={self.token}&debug=1"
        r = self.request("post", url, data)
        return r.json()

    # 二次验证
    def authsucc(self, USERID):
        url = f"{self._url}/user/authsucc?access_token={self.token}&userid={USERID}&debug=1"
        r = self.request("get", url)
        return r.json()

    # 邀请成员
    def invite_user(self, data):
        url = f"{self._url}/batch/invite?access_token={self.token}&debug=1"
        r = self.request("post", url, data)
        return r.json()

    # 获取加入企业二维码
    def get_join_qrcode(self):
        url = f"{self._url}/corp/get_join_qrcode?access_token={self.token}&debug=1"
        r = self.request("get", url)
        return r.json()

    # 获取企业活跃成员数
    def get_active_stat(self, data):
        url = f"{self._url}/user/get_active_stat?access_token={self.token}&debug=1"
        r = self.request("post", url, data)
        return r.json()

