# 成员接口
from pages.API.wework_api import WeWork


class User(WeWork):
    def create_user(
            self, userid=None, name=None, alias=None, mobile=None, department=1, order=None, position=None, gender=None,
            email=None, is_leader_in_dept=None, enable=None, avatar_mediaid=None, telephone=None, address=None,
            main_department=None, extattr=None, to_invite=None, external_position=None, external_profile=None
    ):
        """
        创建成员（必须：T；非必须：F）
        :param userid: T;成员UserID。对应管理端的帐号，企业内必须唯一。不区分大小写，长度为1~64个字节。只能由数字、字母和“_-@.”四种字符组成，且第一个字符必须是数字或字母。
        :param name: T;成员名称。长度为1~64个utf8字符
        :param alias: F;成员别名。长度1~32个utf8字符
        :param mobile: F;手机号码。企业内必须唯一，mobile/email二者不能同时为空
        :param department: T;成员所属部门id列表,不超过100个
        :param order: F;部门内的排序值，默认为0，成员次序以创建时间从小到大排列。个数必须和参数department的个数一致，数值越大排序越前面。有效的值范围是[0, 2^32)
        :param position: F;职务信息。长度为0~128个字符
        :param gender: F;性别。1表示男性，2表示女性
        :param email: F;邮箱。长度6~64个字节，且为有效的email格式。企业内必须唯一，mobile/email二者不能同时为空
        :param is_leader_in_dept: F;个数必须和参数department的个数一致，表示在所在的部门内是否为上级。1表示为上级，0表示非上级。在审批等应用里可以用来标识上级审批人
        :param enable: F;启用/禁用成员。1表示启用成员，0表示禁用成员
        :param avatar_mediaid: F;
        :param telephone: F;座机。32字节以内，由纯数字、“-”、“+”或“,”组成。
        :param address: F;地址。长度最大128个字符
        :param main_department: F;主部门
        :param extattr: F;自定义字段。自定义字段需要先在WEB管理端添加，见扩展属性添加方法，否则忽略未知属性的赋值。与对外属性一致，不过只支持type=0的文本和type=1的网页类型，详细描述查看对外属性
        :param to_invite: F;是否邀请该成员使用企业微信（将通过微信服务通知或短信或邮件下发邀请，每天自动下发一次，最多持续3个工作日），默认值为true。
        :param external_position: F;对外职务，如果设置了该值，则以此作为对外展示的职务，否则以position来展示。长度12个汉字内
        :param external_profile: F;成员对外属性，字段详情见对外属性
        :return: rensponse响应信息
        """
        data = {
            "userid": userid,
            "name": name,
            "alias": alias,
            "mobile": mobile,
            "department": department,
            "order": order,
            "position": position,
            "gender": gender,
            "email": email,
            "is_leader_in_dept": is_leader_in_dept,
            "enable": enable,
            "avatar_mediaid": avatar_mediaid,
            "telephone": telephone,
            "address": address,
            "main_department": main_department,
            "extattr": extattr,
            "to_invite": to_invite,
            "external_position": external_position,
            "external_profile": external_profile
        }
        print(f"创建成员上送参数为:{data}")
        url = f"{self._url}/user/create?access_token={self.token}"
        r = self.request("post", url, data)
        return r.json()

    def get_user(self, USERID):
        """
        读取成员信息
        :param USERID:成员ID
        :return:errcode:0,errmsg:ok,成员详细信息
        """
        url = f"{self._url}/user/get?access_token={self.token}&userid={USERID}"
        r = self.request("get", url)
        return r.json()

    def updata_user(
        self, userid=None, new_userid=None, name=None, alias=None, mobile=None, department=None, order=None,
        position=None, gender=None, email=None, is_leader_in_dept=None, enable=None, avatar_mediaid=None, telephone=None,
        address=None, main_department=None, extattr=None, external_position=None, external_profile=None
    ):
        """
        更新成员（必须：T；非必须：F）
        :param userid: T;成员UserID。对应管理端的帐号，企业内必须唯一。不区分大小写，长度为1~64个字节
        :param new_userid: F;如果userid由系统自动生成，则仅允许修改一次。新值可由new_userid字段指定
        :param name: F;成员名称。长度为1~64个utf8字符
        :param alias: F;别名。长度为1-32个utf8字符
        :param mobile: F;手机号码。企业内必须唯一。若成员已激活企业微信，则需成员自行修改（此情况下该参数被忽略，但不会报错）
        :param department: F;成员所属部门id列表，不超过100个
        :param order: F;部门内的排序值，默认为0。当有传入department时有效。数量必须和department一致，数值越大排序越前面。有效的值范围是[0, 2^32)
        :param position: F;职务信息。长度为0~128个字符
        :param gender: F;性别。1表示男性，2表示女性
        :param email: F;邮箱。长度不超过64个字节，且为有效的email格式。企业内必须唯一。若是绑定了腾讯企业邮箱的企业微信，则需要在腾讯企业邮箱中修改邮箱（此情况下该参数被忽略，但不会报错）
        :param is_leader_in_dept: F;上级字段，个数必须和department一致，表示在所在的部门内是否为上级。
        :param enable: F;启用/禁用成员。1表示启用成员，0表示禁用成员
        :param avatar_mediaid: F;成员头像的mediaid，通过素材管理接口上传图片获得的mediaid
        :param telephone: F;座机。由1-32位的纯数字、“-”、“+”或“,”组成
        :param address: F;地址。长度最大128个字符
        :param main_department: F;主部门
        :param extattr: F;自定义字段。自定义字段需要先在WEB管理端添加，见扩展属性添加方法，否则忽略未知属性的赋值。与对外属性一致，不过只支持type=0的文本和type=1的网页类型，详细描述查看对外属性
        :param external_position: F;对外职务，如果设置了该值，则以此作为对外展示的职务，否则以position来展示。不超过12个汉字
        :param external_profile: F;成员对外属性，字段详情见对外属性
        :return: rensponse响应信息
        """
        data = {
            "userid": userid,
            "new_userid": new_userid,
            "name": name,
            "department": department,
            "order": order,
            "position": position,
            "mobile": mobile,
            "gender": gender,
            "email": email,
            "is_leader_in_dept": is_leader_in_dept,
            "enable": enable,
            "avatar_mediaid": avatar_mediaid,
            "telephone": telephone,
            "alias": alias,
            "address": address,
            "main_department": main_department,
            "extattr": extattr,
            "external_position": external_position,
            "external_profile": external_profile,
        }
        print(f"更新成员上送参数为:{data}")
        url = f"{self._url}/user/update?access_token={self.token}"
        r = self.request("post", url, data)
        return r.json()

    def delete_user(self, USERID):
        """
        删除成员
        :param USERID: 成员ID
        :return: errcode:0,errmsg:deleted
        """
        url = f"{self._url}/user/delete?access_token={self.token}&userid={USERID}"
        r = self.request("get", url)
        return r.json()

    def batch_delete_users(self, userlist):
        """
        批量删除成员
        :param data: userlist
        :return: errcode:0,errmsg:deleted
        """
        data = {
            "useridlist": userlist
        }
        url = f"{self._url}/user/batchdelete?access_token={self.token}"
        r = self.request("post", url, data)
        return r.json()

    def get_simple_list(self, ID, FETCH_CHILD=None):
        """
        获取部门成员简单信息
        :param ID: T:获取的部门id
        :param FETCH_CHILD: F:是否递归获取子部门下面的成员：1-递归获取，0-只获取本部门
        :return: errcode:0,errmsg:ok,userlist:[]
        """
        url = f"{self._url}/user/simplelist?access_token={self.token}&department_id={ID}&fetch_child={FETCH_CHILD}"
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

    def get_list(self, DEPARTMENT_ID, FETCH_CHILD=None):
        """
        获取部门成员详情
        :param DEPARTMENT_ID:T:获取的部门id
        :param FETCH_CHILD: F:1/0：是否递归获取子部门下面的成员
        :return: errcode:0,errmsg:ok,userlist:[]
        """
        url = f"{self._url}/user/list?access_token={self.token}&department_id={DEPARTMENT_ID}&fetch_child={FETCH_CHILD}"
        r = self.request("get", url)
        return r.json()

    # userid转openid
    def convert_to_openid(self, data):
        url = f"{self._url}/user/convert_to_openid?access_token={self.token}"
        r = self.request("post", url, data)
        return r.json()

    # openid转userid
    def convert_to_userid(self, data):
        url = f"{self._url}/user/convert_to_userid?access_token={self.token}"
        r = self.request("post", url, data)
        return r.json()

    # 二次验证
    def authsucc(self, USERID):
        url = f"{self._url}/user/authsucc?access_token={self.token}&userid={USERID}"
        r = self.request("get", url)
        return r.json()

    # 邀请成员
    def invite_user(self, data):
        url = f"{self._url}/batch/invite?access_token={self.token}"
        r = self.request("post", url, data)
        return r.json()

    # 获取加入企业二维码
    def get_join_qrcode(self):
        url = f"{self._url}/corp/get_join_qrcode?access_token={self.token}"
        r = self.request("get", url)
        return r.json()

    # 获取企业活跃成员数
    def get_active_stat(self, data):
        url = f"{self._url}/user/get_active_stat?access_token={self.token}"
        r = self.request("post", url, data)
        return r.json()
