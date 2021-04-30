from flask import current_app, jsonify, g, request
from app.libs.redprint import Redprint
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.models.user import User, user_schema, users_schema
from app.models.role import Role
from app.models.base import db
from app.models.opLog import OperateLog
from app.libs.token_auth import login_required
from app.libs.status_code import Success, ParameterException, DeleteSuccess
from marshmallow import ValidationError
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
import uuid

api = Redprint('user')


@api.route('/login', methods=['POST'])
def login():
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
                                identity['holderId'],
                                expiration)
    user = User.query.filter_by(username=data['username']).first()
    with db.auto_commit():
        user.lastLoginIp = request.remote_addr
    t = {
        'token': token.decode('ascii')
    }
    OperateLog.write_log(user.id, '账户操作', '登录')
    return jsonify(t)


@api.route('/logout')
def logout():
    return 'ok'


@api.route('/get-userinfo')
@login_required(['admin', 'hr', 'employee'])
def get_userinfo():
    uid = g.user.uid
    user_info = User.query.filter_by(id=uid).first_or_404()
    user_info_result = user_schema.dump(user_info)
    return user_info_result


@api.route('/list')
@login_required(['admin'])
def get_user_list():
    account = request.args.get('account')
    holder_id = request.args.get('holderId')
    if account:
        user_list = User.query.filter(and_(User.username.like(f'%{account}%'), User.status == 1))
    elif holder_id:
        user_list = User.query.filter_by(holderId=holder_id).all()
    else:
        user_list = User.query.filter_by().all()
    result = users_schema.dump(user_list)
    for index, item in enumerate(result):
        if user_list[index].holder_info:
            item['holder'] = user_list[index].holder_info.name
            item['phone'] = user_list[index].holder_info.phone
        else:
            if 'admin' in g.user.role:
                item['holder'] = '超级管理员'
    return jsonify(result)


@api.route('/get-user-tags-list')
@login_required(['admin'])
def get_user_tags_list():
    username = request.args.get('username')
    if username:
        user_list = User.query.filter(User.username.like(f'%{username}%'), User.status == 1).all()
    else:
        user_list = User.query.filter_by().all()
    result = []
    for item in user_list:
        json = {
            'value': item.id,
            'label': item.username
        }
        result.append(json)
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
    try:
        with db.auto_commit():
            user = User()
            user.username = data['username']
            user.password = data['password']
            if data['holderId']:
                user.holderId = data['holderId']
            user.roles = roles_list
    except IntegrityError:
        return ParameterException(msg="用户名已存在")
    OperateLog.write_log(g.user.uid, '账户操作', f'添加账户{user.username}')
    return Success()


@api.route('/modify-password', methods=['POST'])
@login_required(['admin'])
def modify_user():
    json_data = request.get_json()
    if not json_data:
        return ParameterException()
    if not json_data.get('id'):
        return ParameterException(msg="缺少要修改账户的ID")
    try:
        account_id = int(json_data.get('id'))
    except ValueError:
        return ParameterException("账户ID格式错误")
    user = User.query.filter_by(id=account_id).first_or_404()
    del json_data['id']
    try:
        data = user_schema.load(json_data, partial=True)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    with db.auto_commit():
        user.password = data['password']
    OperateLog.write_log(g.user.uid, '账户操作', f'修改账户{user.username}的密码')
    return Success()


@api.route('/change-password', methods=['POST'])
@login_required(['admin', 'hr'])
def change_password():
    json_data = request.get_json()
    if not json_data:
        ParameterException(msg="数据为空")
    try:
        data = user_schema.load(json_data, partial=True)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    user = User.query.filter_by(id=g.user.uid).first_or_404()
    with db.auto_commit():
        user.password = data['password']
    return Success()


@api.route('/delete', methods=['POST'])
@login_required(['admin'])
def delete_user():
    json_data = request.get_json()
    if not json_data:
        return ParameterException(msg="数据为空")
    user_id = json_data.get('id')
    if not user_id:
        return ParameterException(msg="缺少账号ID")
    account = User.query.filter_by(id=user_id).first_or_404()
    with db.auto_commit():
        db.session.delete(account)
    return DeleteSuccess()


def generate_auth_token(uid, username, roles, holder_id, expiration=7200):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps({
        'uid': uid,
        'username': username,
        'roles': [role.name for role in roles],
        'holder_id': holder_id
    })
