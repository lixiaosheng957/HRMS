from flask import current_app, jsonify, g, request

from app.libs.expection import DatabaseRecordRepeat
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.department import Department, department_schema, departments_schema
from app.models.opLog import OperateLog
from app.libs.token_auth import login_required
from app.libs.status_code import Success, ParameterException, DeleteSuccess
from marshmallow import ValidationError
from sqlalchemy import and_

api = Redprint('department')


@api.route("/add", methods=['POST'])
@login_required(["admin"])
def add_department():
    json_data = request.get_json()
    # print(json_data)
    if not json_data:
        return ParameterException()
    try:
        data = department_schema.load(json_data)
        if Department.query.filter_by(name=data['name']).first():
            raise DatabaseRecordRepeat()
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    except DatabaseRecordRepeat as err:
        return ParameterException(msg=err.msg)
    with db.auto_commit():
        department = Department()
        for key, value in data.items():
            setattr(department, key, value)
        db.session.add(department)
    OperateLog.write_log(g.user.uid, '部门操作', f'添加{department.name}部门')
    return Success()


@api.route('/get-department-list')
@login_required(["admin", 'hr'])
def get_department_list():
    for_select_tag = request.args.get('selectTag')
    if for_select_tag:
        keyword = request.args.get('nameKeyword')
        department_list = Department.query.filter(
            and_(Department.name.like(f'%{keyword}%'), Department.status == 1)).all()
        departments_select = []
        for item in department_list:
            json = {'value': item.id, 'label': item.name}
            departments_select.append(json)

        return jsonify(departments_select)
    else:
        department_list = Department.query.filter_by().all()
        result = departments_schema.dump(department_list)
        return_json = []
        for index, item in enumerate(result):
            if not item['parentId']:
                return_json.append(item)
        for item in return_json:
            department_serializing(item)
        return jsonify(return_json)


@api.route('/get')
@login_required(["admin", 'hr'])
def get_department():
    department_id = request.args.get('id')
    if not department_id:
        return ParameterException()
    department = Department.query.filter_by(id=department_id).first_or_404()
    result = department_schema.dump(department)
    return jsonify(result)


@api.route('/delete', methods=['POST'])
@login_required(["admin"])
def delete_department():
    department_id = request.get_json()['id']
    if not department_id:
        return ParameterException()
    department = Department.query.filter_by(id=department_id).first_or_404()
    if len(department.children) > 0:
        return ParameterException(msg="该部门员工数不为零，不能删除")
    with db.auto_commit():
        department.status = 0
    OperateLog.write_log(g.user.uid, '部门操作', f'删除{department.name}部门')
    return DeleteSuccess()


@api.route('/modify', methods=['POST'])
@login_required(["admin", 'hr'])
def modify_department():
    json_data = request.get_json()
    print(json_data)
    if not json_data:
        return ParameterException()
    try:
        data = department_schema.load(json_data)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    department = Department.query.filter_by(id=data['id']).first_or_404()
    with db.auto_commit():
        for key, value in data.items():
            if value and key != "id":
                setattr(department, key, value)
    OperateLog.write_log(g.user.uid, '部门操作', f'修改{department.name}部门')
    return Success()


def department_serializing(target):
    if len(target['children']) == 0:
        temp = Department.query.filter_by(id=target['id']).first()
        target['number'] = len(temp.employee)
        target['label'] = temp.name
        return target['number']
    else:
        temp = Department.query.filter_by(id=target['id']).first()
        target['number'] = len(temp.employee)
        target['label'] = temp.name
        for item in target['children']:
            target['number'] = target['number'] + department_serializing(item)
        return target['number']
