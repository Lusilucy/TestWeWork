import pytest

from utils.utils import Utils


@pytest.fixture
def member_data():
    """
    fake成员信息
    :return: [姓名，帐号，手机号，邮箱]
    """
    name = Utils.fake.name()
    userid = Utils.fake.userid()
    phone = Utils.fake.mobile()
    email = Utils.fake.email()
    return [name, userid, phone, email]
