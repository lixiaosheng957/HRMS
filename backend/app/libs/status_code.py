from app.libs.request_status import APIException


class Success(APIException):
    code = 201
    msg = 'ok'
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = 1
    msg = '删除成功'


class ServerError(APIException):
    code = 500
    msg = '系统异常'
    error_code = 999


class ClientTypeError(APIException):
    code = 400
    msg = 'client is invalid'


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = '数据库不存在此记录'
    error_code = 1001


class AuthFailed(APIException):
    code = 401
    error_code = 1005
    msg = 'authorization failed'


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = '没有访问权限'

