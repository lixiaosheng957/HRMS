from flask import current_app, jsonify, g, request
from app.libs.redprint import Redprint
from app.models.employee import Employee, employee_schema, employees_schema
from app.models.base import db
from app.libs.token_auth import login_required
from app.libs.expection import DatabaseRecordRepeat
from app.libs.status_code import Success, ParameterException, DeleteSuccess
from marshmallow import ValidationError

api = Redprint('employee')


@api.route('/add', methods=['POST'])
@login_required(['admin'])
def add_employee():
    json_data = request.get_json()
    if not json_data:
        return ParameterException()
    try:
        data = employee_schema.load(json_data)
        if Employee.query.filter_by(idCard=data['idCard']).first():
            raise DatabaseRecordRepeat()
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    except DatabaseRecordRepeat as err:
        return ParameterException(msg=err.msg)
    with db.auto_commit():
        employee = Employee()
        for key, value in data.items():
            setattr(employee, key, value)
        db.session.add(employee)
    return Success()


@api.route('/modify', methods=['POST'])
@login_required(['admin'])
def modify_employee():
    json_data = request.get_json()
    if not json_data:
        return ParameterException()
    try:
        data = employee_schema.load(json_data)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    employee = Employee.query.filter_by(id=data['id']).first_or_404()
    with db.auto_commit():
        for key, value in data.items():
            setattr(employee, key, value)
    return Success()


@api.route('/getlist')
@login_required(['admin'])
def get_employee_list():
    employee_type = request.args.get('type')
    is_leave = request.args.get('leave')
    department_id = None
    if request.args.get('departmentId'):
        department_id = int(request.args.get('departmentId'))
    if employee_type and department_id and not is_leave:
        employees_list = Employee.query.filter_by(type=employee_type, departmentId=department_id).all()
    elif is_leave and department_id and not employee_type:
        employees_list = Employee.query.filter_by(workState="离职", departmentId=department_id).all()
    else:
        employees_list = Employee.query.filter_by().all()
    result = employees_schema.dump(employees_list)
    for index, item in enumerate(result):
        item['job'] = employees_list[index].job_level.name
    return jsonify(result)


@api.route('/get-employee')
@login_required(['admin'])
def get_employee():
    employee_id = int(request.args.get('id'))
    employee = Employee.query.filter_by(id=employee_id).first_or_404()
    result = employee_schema.dump(employee)
    return jsonify(result)


@api.route('/search-by-name-or-id')
@login_required(['admin'])
def search_by_name_or_id():
    keyword = request.args.get('keyword')
    if keyword:
        try:
            employee_id = int(keyword)
            employee = Employee.query.filter_by(id=employee_id).first_or_404()
            result = employee_schema.dump(employee)
            return jsonify(result)
        except ValueError:
            employee = Employee.query.filter(Employee.name.like(f'%{keyword}%')).first_or_404()
            result = employee_schema.dump(employee)
            return jsonify(result)


@api.route('/delete', methods=['POST'])
@login_required(['admin'])
def delete_employee():
    employee_id = request.get_json()['id']
    if not employee_id:
        return ParameterException()
    employee = Employee.query.filter_by(id=employee_id).first_or_404()
    with db.auto_commit():
        employee.status = 0
    return DeleteSuccess()
