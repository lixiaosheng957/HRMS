class DatabaseRecordRepeat(Exception):
    def __init__(self, msg="重复记录"):
        self.msg = msg


class FormatError(Exception):
    def __init__(self, msg="格式错误"):
        self.msg = msg
