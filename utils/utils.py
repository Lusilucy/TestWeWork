# 工具类
import json
import random
import yaml
import pystache
from faker import Faker


class Utils:
    @classmethod
    def get_data(self, file, context=None):
        """
        获取数据
        :param file: 文件路径
        :param context: 替换json文件中形参的实参
        :return: yaml返回python格式数据，json返回字典格式数据
        """
        # yaml文件解析
        if "yaml" in file:
            with open(file, encoding="utf-8") as f:
                return yaml.safe_load(f)

        # json文件解析
        elif "json" in file:
            with open(file) as d:
                # 替换json文件中参数
                data = pystache.render(f'{d.read()}', context)
                # 将json转换为字典格式输出
                return json.loads(data)

    @classmethod
    def dump_data(self, data, file_path):
        """
        封装存储数据方法
        :param data: 待存储的数据
        :param file_path: 存放路径（yaml文件格式）
        :return: 上传
        """
        with open(file_path, "w", encoding="utf-8") as f:
            return yaml.safe_dump(data, f)

    @classmethod
    def member_data(cls):
        """
        fake成员信息
        :return: [姓名，帐号，手机号，邮箱]
        """
        name = cls.fake.name()
        userid = cls.fake.userid()
        phone = cls.fake.mobile()
        email = cls.fake.email()
        return [name, userid, phone, email]

    # fake工具
    class fake:
        # 实例化Faker（中文）
        fake = Faker("zh_CN")

        # fake 姓名
        @classmethod
        def name(cls):
            return cls.fake.name()

        # fake 手机号
        @classmethod
        def mobile(cls):
            return cls.fake.phone_number()

        # fake 地址
        @classmethod
        def address(cls):
            return cls.fake.address()

        # fake 成员ID
        @classmethod
        def userid(cls):
            # return cls.fake.pyint(min_value=1, max_value=9999999999, step=1)
            return random.randrange(1, 9999999999)

        # fake 性别 （1男,2女）
        @classmethod
        def gender(cls):
            return random.choice([1, 2])
            # return cls.fake.pyint(min_value=1, max_value=2)

        @classmethod
        def email(cls):
            return cls.fake.email()

        @classmethod
        def bool(cls):
            return random.choice([True, False])


