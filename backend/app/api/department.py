from flask import current_app, jsonify, g, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.department import Department, department_schema, departments_schema
from app.libs.token_auth import login_required
from app.libs.status_code import Success, ParameterException
from marshmallow import ValidationError
from sqlalchemy import and_, or_

api = Redprint('department')


@api.route("/add", methods=['POST'])
@login_required(["admin"])
def add_department():
    json_data = request.get_json()
    if not json_data:
        return ParameterException()
    try:
        data = department_schema.load(json_data)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    with db.auto_commit():
        department = Department()
        for key, value in data.items():
            setattr(department, key, value)
        db.session.add(department)
    return Success()


@api.route('/get-department-list')
@login_required(["admin"])
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
        for index, item in enumerate(result):
            if not item['isParent']:
                del result[index]
            else:
                department_serializing(item)
        return jsonify(result)


@api.route('/delete')
@login_required(["admin"])
def delete_department():
    department_id = request.get_json()['id']
    if not department_id:
        return ParameterException()
    department = Department.query.filter_by(id=department_id).first_or_404()
    with db.auto_commit():
        department.status = 0
    return Success()


@api.route('modify')
@login_required(["admin"])
def modify_department():
    json_data = request.get_json()
    if not json_data:
        return ParameterException()
    try:
        data = department_schema.load(json_data)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    department = Department.query.filter_by(id=data['id']).first_or_404()
    with db.auto_commit():
        for key, value in data.items():
            setattr(department, key, value)
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
