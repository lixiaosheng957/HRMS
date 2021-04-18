from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app, request, g
from app.libs.status_code import AuthFailed, Forbidden
from functools import wraps
from collections import namedtuple

User = namedtuple('User', ['uid', 'username', 'role', 'holderId'])


def login_required(allow_roles: list = None):
    def warp_function(view_func):
        @wraps(view_func)
        def decorated_view(*args, **kwargs):
            try:
                token = request.headers['Access_Token']
            except KeyError:
                raise AuthFailed()
            user_info = verify_auth_token(token, allow_roles)
            if not user_info:
                return AuthFailed()
            g.user = user_info
            return view_func(*args, **kwargs)

        return decorated_view

    return warp_function


def verify_auth_token(token, allow_roles):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    uid = data['uid']
    username = data['username']
    roles = data['roles']
    holder_id = data['holder_id']
    if allow_roles:
        allow = set(allow_roles) & set(roles)
        if not allow:
            raise Forbidden()
    return User(uid, username, roles, holder_id)
