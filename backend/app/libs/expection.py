class DatabaseRecordRepeat(Exception):
    def __init__(self, msg="重复记录"):
        self.msg = msg
