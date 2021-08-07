class MyError(Exception):
    pass


class NotFoundError(MyError):
    pass


class NoneMemberException(MyError):
    pass
