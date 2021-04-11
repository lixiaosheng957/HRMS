from flask import current_app, jsonify, g, request
from app.libs.redprint import Redprint
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.models.user import User, user_schema, users_schema
from app.models.role import Role
from app.models.base import db
from app.libs.token_auth import login_required
from app.libs.status_code import Success, ParameterException
from marshmallow import ValidationError

api = Redprint('user')


@api.route('/login', methods=['POST'])
def login():
    # form = ClientForm().validate_for_api()
    json_data = request.get_json()
    if not json_data:
        return ParameterException()
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    identity = User.verify(data['username'], data['password'])
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity['uid'],
                                data['username'],
                                identity['roles'],
                                expiration)
    user = User.query.filter_by(username=data['username']).first()
    with db.auto_commit():
        user.lastLoginIp = request.remote_addr
    t = {
        'token': token.decode('ascii')
    }
    return jsonify(t)


@api.route('/logout')
def logout():
    return 'ok'


@api.route('/get-userinfo')
@login_required(['admin'])
def get_userinfo():
    uid = g.user.uid
    user_info = User.query.filter_by(id=uid).first_or_404()
    user_info_result = user_schema.dump(user_info)
    return user_info_result


@api.route('/list')
@login_required(['admin'])
def get_user_list():
    current_page = int(request.args.get('currentPage'))
    page_size = int(request.args.get('pageSize'))
    user_list = User.query.paginate(current_page, page_size).items
    result = users_schema.dump(user_list)
    return jsonify(result)


@api.route('/add', methods=['POST'])
@login_required(['admin'])
def add_user():
    json_data = request.get_json()
    del json_data['confirmPassword']
    if not json_data:
        return ParameterException()
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    roles_list = []
    for item in data['roles']:
        role = Role.query.filter_by(name=item['name']).first()
        if role:
            roles_list.append(role)
        else:
            return ParameterException(msg="没有此项权限!")
    with db.auto_commit():
        user = User()
        user.username = data['username']
        user.password = data['password']
        user.holder = data['holder']
        user.phone = data['phone']
        user.roles = roles_list
    return Success()


@api.route('/modify')
@login_required(['admin'])
def modify_user():
    json_data = request.get_json()
    if not json_data:
        return ParameterException()
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    user = User.query.filter_by(id=data['id']).first_or_404()
    with db.auto_commit():
        for key, value in data.items():
            setattr(user, key, value)

    return Success()


def generate_auth_token(uid, username, roles, expiration=7200):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps({
        'uid': uid,
        'username': username,
        'roles': [role.name for role in roles]
    })
