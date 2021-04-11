import time


class AjaxJson:
    def __init__(self):
        pass

    @staticmethod
    def json_fn(result=None, success=True, message='操作成功', code=200, **kwargs):
        if result is None:
            result = {}
        return {"code": code, "message": message, "success": success, "result": result, **kwargs,
                "timestamp": int(round(time.time() * 1000))}
