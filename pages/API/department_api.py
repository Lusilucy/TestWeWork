# 部门接口
from pages.API.wework_api import WeWork


class Department(WeWork):
    def create_department(self, data):
        """
        创建部门
        :param data: 上送信息
        :return: response
        """
        url = f"{self._url}/department/create?access_token={self.token}"
        r = self.request("post", url, data)
        return r.json()

    def update_department(self, data):
        """
        更新部门
        :param data: 上送信息
        :return: response
        """
        url = f"{self._url}/department/update?access_token={self.token}"
        r = self.request("post", url, data)
        return r.json()

    def delete_department(self, ID=None):
        """
        删除部门
        :param ID: 部门id
        :return: response
        """
        url = f"{self._url}/department/delete?access_token={self.token}&id={ID}"
        r = self.request("get", url)
        return r.json()

    def get_department_list(self, ID=None):
        """
        获取部门列表
        :param ID: 部门id
        :return: response
        """
        url = f"{self._url}/department/list?access_token={self.token}&id={ID}"
        r = self.request("get", url)
        return r.json()

    def clear_departments(self, ID=None):
        """
        清理环境，删除除主部门外的所有部门
        :param ID: 部门ID
        :return: response
        """
        ids = self.jpath(self.get_department_list(ID), "$..id")
        for i in ids:
            if i != 1:
                self.delete_department(i)
