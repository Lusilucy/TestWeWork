from pages.API.wework_api import WeWork


class Department(WeWork):
    def create_department(self, data):
        url = f"{self._url}/department/create?access_token={self.token}&debug=1"
        r = self.request("post", url, data)
        return r.json()

    def update_department(self, data):
        url = f"{self._url}/department/update?access_token={self.token}&debug=1"
        r = self.request("post", url, data)
        return r.json()

    def delete_depatment(self, ID=None):
        url = f"{self._url}/department/delete?access_token={self.token}&id={ID}&debug=1"
        r = self.request("get", url)
        return r.json()

    def get_department_list(self, ID=None):
        url = f"{self._url}/department/list?access_token={self.token}&id={ID}&debug=1"
        r = self.request("get", url)
        return r.json()

    def clear_departments(self, ID=None):
        ids = self.jpath(self.get_department_list(ID), "$..id")
        for i in ids:
            if i != 1:
                self.delete_depatment(i)
