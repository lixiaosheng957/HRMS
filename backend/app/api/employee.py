from flask import current_app, jsonify, g, request
from app.libs.redprint import Redprint
from app.models.employee import Employee, employee_schema, employees_schema
from app.models.employee_transfer import EmployeeTransfer, employee_transfer_schema, employee_transfers_schema
from app.models.base import db
from app.models.opLog import OperateLog
from app.libs.token_auth import login_required
from app.libs.expection import DatabaseRecordRepeat
from app.libs.status_code import Success, ParameterException, DeleteSuccess
from marshmallow import ValidationError
from sqlalchemy import and_

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
            raise DatabaseRecordRepeat("身份号重复")
        if Employee.query.filter_by(workId=data['workId']).first():
            raise DatabaseRecordRepeat(msg="工号重复")
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    except DatabaseRecordRepeat as err:
        return ParameterException(msg=err.msg)
    with db.auto_commit():
        employee = Employee()
        for key, value in data.items():
            setattr(employee, key, value)
        db.session.add(employee)
    OperateLog.write_log(g.user.uid, '员工操作', f'添加员工{employee.name}')
    return Success()


@api.route('/modify', methods=['POST'])
@login_required(['admin'])
def modify_employee():
    json_data = request.get_json()
    if not json_data:
        return ParameterException()
    try:
        data = employee_schema.load(json_data, partial=True)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    employee = Employee.query.filter_by(id=data['id']).first_or_404()
    with db.auto_commit():
        for key, value in data.items():
            if key in ['wedlock', 'phone', 'email', 'address']:
                setattr(employee, key, value)
    OperateLog.write_log(g.user.uid, '员工操作', f'修改员工{employee.name}')
    return Success()


@api.route('/getlist')
@login_required(['admin'])
def get_employee_list():
    employees_list = None
    if not request.args:
        employees_list = Employee.query.filter_by(workState="在职").all()
    else:
        tags = request.args.get('tags')
        name = request.args.get('name')
        employee_id = request.args.get('id')
        department_id = request.args.get('departmentId')
        job_id = request.args.get('jobId')
        employee_type = request.args.get('type')
        if tags:
            employees_list = Employee.query.filter(
                and_(Employee.name.like(f'%{name}%'), Employee.workState == "在职", Employee.status == 1))
            result = []
            for item in employees_list:
                json = {
                    'label': item.name + ' ' + '(' + item.department.name + ')',
                    'value': item.id
                }
                result.append(json)
            return jsonify(result)
        if department_id:
            if department_id and employee_id:
                employees_list = Employee.query.filter_by(id=employee_id, departmentId=department_id,
                                                          workState="在职").all()
            elif department_id and job_id:
                employees_list = Employee.query.filter_by(departmentId=department_id, jobLevelId=job_id,
                                                          workState="在职").all()
            elif department_id and employee_type:
                employees_list = Employee.query.filter_by(departmentId=department_id, type=employee_type,
                                                          workState="在职").all()
            else:
                employees_list = Employee.query.filter_by(departmentId=department_id, workState="在职").all()
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
    result['department'] = employee.department.name
    result['job'] = employee.job_level.name
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
    OperateLog.write_log(g.user.uid, '员工操作', f'删除员工{employee.name}')
    return DeleteSuccess()


@api.route('/transfer', methods=['post'])
@login_required(['admin', 'hr'])
def employee_transfer():
    json_data = request.get_json()
    if not json_data:
        return ParameterException()
    try:
        data = employee_transfer_schema.load(json_data)
        print(type(data))
    except ValidationError as err:
        return ParameterException(err.messages)
    with db.auto_commit():
        transfer_record = EmployeeTransfer()
        update_employee = Employee.query.filter_by(id=data['employeeId']).first_or_404()
        for key, value in data.items():
            setattr(transfer_record, key, value)
        if 'transferDepartmentId' in data and 'transferJobId' in data:
            update_employee.departmentId = data['transferDepartmentId']
            update_employee.jobLevelId = data['transferJobId']
        if 'contractBeginDate' in data and 'contractEndDate' in data:
            update_employee.contractBeginDate = data['contractBeginDate']
            update_employee.contractEndDate = data['contractEndDate']
        if data['transferType'] == '试用期转正':
            if update_employee.type == '试用员工':
                update_employee.type = '正式员工'
            else:
                return ParameterException(msg="变动类型错误")
        if data['transferType'] == '实习期转试用':
            if update_employee.type == '实习员工':
                update_employee.type = '试用员工'
            else:
                return ParameterException(msg="变动类型错误")
        transfer_record.operatorId = g.user.uid
        transfer_record.beforeTransferDepartmentId = update_employee.departmentId
        transfer_record.beforeTransferJobId = update_employee.jobLevelId
        transfer_record.beforeContractBeginDate = update_employee.contractBeginDate
        transfer_record.beforeContractEndDate = update_employee.contractEndDate
        db.session.add(transfer_record)
    OperateLog.write_log(g.user.uid, '员工操作', f'变动员工{update_employee.name}')
    return Success()


@api.route('/move', methods=['post'])
@login_required(['admin'])
def employee_move():
    pass


@api.route('/get-transfer-records')
@login_required(['admin', 'hr'])
def get_transfer_records():
    is_for_me = request.args.get('mine')
    if is_for_me:
        uid = g.user.uid
        transfer_records = EmployeeTransfer.query.filter_by(operatorId=uid).all()
    else:
        transfer_records = EmployeeTransfer.query.filter_by().all()
    result = employee_transfers_schema.dump(transfer_records)
    return jsonify(result)
