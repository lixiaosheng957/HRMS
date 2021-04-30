from flask import current_app, jsonify, g, request
from app.libs.redprint import Redprint
from app.models.employee import Employee, employee_schema, employees_schema
from app.models.employee_transfer import EmployeeTransfer, employee_transfer_schema, employee_transfers_schema
from app.models.base import db
from app.models.department import Department
from app.models.job_level import JobLevel
from app.models.employee_move import EmployeeMoveRecord, employee_move_record_schema, employee_move_records_schema
from app.models.opLog import OperateLog
from app.libs.token_auth import login_required
from app.libs.expection import DatabaseRecordRepeat
from app.libs.status_code import Success, ParameterException, DeleteSuccess
from marshmallow import ValidationError
from sqlalchemy import and_
import datetime

api = Redprint('employee')


@api.route('/add', methods=['POST'])
@login_required(['admin', 'hr'])
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
@login_required(['admin', 'hr'])
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
@login_required(['admin', 'hr'])
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
            if name:
                employees_list = Employee.query.filter(
                    and_(Employee.name.like(f'%{name}%'), Employee.workState == "在职", Employee.status == 1))
            else:
                employees_list = Employee.query.filter_by().all()
            result = []
            for item in employees_list:
                json = {
                    'label': item.name + ' ' + '(' + item.department.name + ')',
                    'value': item.id
                }
                result.append(json)
            return jsonify(result)
        params = []
        if department_id:
            params.append(Employee.departmentId == department_id)
        if employee_id:
            params.append(Employee.id == employee_id)
        if job_id:
            params.append(Employee.jobLevelId == job_id)
        if employee_type:
            params.append(Employee.type == employee_type)
        params.append(Employee.workState == '在职')
        params.append(Employee.status == 1)
        employees_list = Employee.query.filter(*params).all()
    result = employees_schema.dump(employees_list)
    for index, item in enumerate(result):
        item['job'] = employees_list[index].job_level.name
    return jsonify(result)


@api.route('/get-employee')
@login_required(['admin', 'hr'])
def get_employee():
    employee_id = int(request.args.get('id'))
    employee = Employee.query.filter_by(id=employee_id).first_or_404()
    result = employee_schema.dump(employee)
    result['department'] = employee.department.name
    result['job'] = employee.job_level.name
    result['transferRecord'] = []
    result['trainingRecord'] = []
    for item in employee.training_record:
        json = {
            'programName': item.training_program.name,
            'programStartDate': item.training_program.beginDate.strftime('%Y-%m-%d'),
            'programEndDate': item.training_program.endDate.strftime('%Y-%m-%d'),
            'isFinish': item.isFinish,
            'assess': item.assess,
            'level': item.level
        }
        result['trainingRecord'].append(json)
    for item in employee.transfer_record:
        json = {
            'transferType': item.transferType,
            'transferDepartment': item.employee_info.department.name,
            'transferJob': item.employee_info.job_level.name,
            'transferTime': item.transferTime.strftime('%Y-%m-%d')
        }
        before_transfer_department = Department.query.filter(Department.id == item.beforeTransferDepartmentId).first()
        if before_transfer_department:
            json['beforeTransferDepartment'] = before_transfer_department.name
        before_transfer_job = JobLevel.query.filter(JobLevel.id == item.beforeTransferJobId).first()
        if before_transfer_job:
            json['beforeTransferJob'] = before_transfer_job.name
        result['transferRecord'].append(json)
    return jsonify(result)


@api.route('/search-by-name-or-id')
@login_required(['admin', 'hr'])
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
    json_data = request.get_json()
    employee_id = json_data.get('id')
    if not employee_id:
        return ParameterException(msg="缺少员工ID")
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
            transfer_record.beforeTransferDepartmentId = update_employee.departmentId
            transfer_record.beforeTransferJobId = update_employee.jobLevelId
            update_employee.departmentId = data['transferDepartmentId']
            update_employee.jobLevelId = data['transferJobId']
        if 'contractBeginDate' in data and 'contractEndDate' in data:
            transfer_record.beforeContractBeginDate = update_employee.contractBeginDate
            transfer_record.beforeContractEndDate = update_employee.contractEndDate
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
        db.session.add(transfer_record)
    OperateLog.write_log(g.user.uid, '员工操作', f'变动员工{update_employee.name}')
    return Success()


@api.route('/move', methods=['post'])
@login_required(['admin', 'hr'])
def employee_move():
    json_data = request.get_json()
    if not json_data:
        return ParameterException(msg="数据为空")
    try:
        data = employee_move_record_schema.load(json_data)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    employee = Employee.query.filter_by(id=data['employeeId']).first()
    if not employee:
        return ParameterException(msg="没有此员工")
    with db.auto_commit():
        employee_move_record = EmployeeMoveRecord()
        for key, value in data.items():
            setattr(employee_move_record, key, value)
        db.session.add(employee_move_record)
        employee.workState = "离职"
    OperateLog.write_log(g.user.uid, '员工操作', f'员工{employee.name}离职')
    return Success()


@api.route('/get-employee-move-list')
@login_required(['admin', 'hr'])
def get_employee_move_list():
    name = request.args.get('name')
    if name:
        employee_move_list = Employee.query.filter(Employee.name.like(f'%{name}%'), Employee.workState == "离职",
                                                   Employee.status == 1).all()
    else:
        employee_move_list = Employee.query.filter_by(workState="离职").all()
    result = employees_schema.dump(employee_move_list)
    for index, item in enumerate(result):
        item['job'] = employee_move_list[index].job_level.name
        item['department'] = employee_move_list[index].department.name
    return jsonify(result)


@api.route('/get-employee-move-detail')
@login_required(['admin', 'hr'])
def get_employee_move_detail():
    employee_id = request.args.get('id')
    if not employee_id:
        return ParameterException(msg="没有指定记录ID")
    record = EmployeeMoveRecord.query.filter_by(employeeId=employee_id).first_or_404()
    result = employee_move_record_schema.dump(record)
    return jsonify(result)


@api.route('/get-transfer-records')
@login_required(['admin', 'hr'])
def get_transfer_records():
    is_for_me = request.args.get('mine')
    employee_id = request.args.get('employeeId')
    if is_for_me:
        uid = g.user.uid
        if employee_id:
            transfer_records = EmployeeTransfer.query.filter_by(operatorId=uid, employeeId=employee_id).all()
        else:
            transfer_records = EmployeeTransfer.query.filter_by(operatorId=uid).all()
    else:
        if employee_id:
            transfer_records = EmployeeTransfer.query.filter_by(employeeId=employee_id).all()
        else:
            transfer_records = EmployeeTransfer.query.filter_by().all()
    result = employee_transfers_schema.dump(transfer_records)
    for index, item in enumerate(result):
        if transfer_records[index].transfer_operator.holderId:
            item['operator'] = transfer_records[index].transfer_operator.account.name
        else:
            item['operator'] = transfer_records[index].transfer_operator.holder
        item['employeeName'] = transfer_records[index].employee_info.name
        item['operateTime'] = transfer_records[index].create_datetime.strftime('%Y-%m-%d %H:%M:%S')
        item['employeeWorkId'] = transfer_records[index].employee_info.workId
    return jsonify(result)


@api.route('/get-transfer-detail')
@login_required(['admin', 'hr'])
def get_transfer_detail():
    record_id = request.args.get('id')
    if not record_id:
        return ParameterException()
    record = EmployeeTransfer.query.filter_by(id=record_id).first_or_404()
    result = employee_transfer_schema.dump(record)
    if record.transfer_operator.holderId:
        result['operator'] = record.transfer_operator.account.name
    else:
        result['operator'] = record.transfer_operator.holder
    result['employeeName'] = record.employee_info.name
    result['operateTime'] = record.create_datetime.strftime('%Y-%m-%d %H:%M:%S')
    result['employeeWorkId'] = record.employee_info.workId
    if record.transferDepartmentId:
        transfer_department = Department.query.filter_by(id=record.transferDepartmentId).first()
        result['transferDepName'] = transfer_department.name
    else:
        result['transferDepName'] = None
    if record.transferJobId:
        transfer_job = JobLevel.query.filter_by(id=record.transferJobId).first()
        result['transferJobName'] = transfer_job.name
    else:
        result['transferJobName'] = None
    if record.beforeTransferDepartmentId:
        before_transfer_dep = Department.query.filter_by(id=record.beforeTransferDepartmentId).first()
        result['beforeTransferDepName'] = before_transfer_dep.name
    else:
        result['beforeTransferDepName'] = None
    if record.beforeTransferJobId:
        before_transfer_job = JobLevel.query.filter_by(id=record.beforeTransferJobId).first()
        result['beforeTransferJobName'] = before_transfer_job.name
    else:
        result['beforeTransferJobName'] = None
    return jsonify(result)


@api.route('/renew', methods=['POST'])
@login_required(['admin','hr'])
def employee_renew():
    json_data = request.get_json()
    a = json_data.get('contractBeginDate')
    if not json_data:
        return ParameterException("数据为空")
    employee_id = json_data.get('employeeId')
    employee = Employee.query.filter_by(id=employee_id).first_or_404()
    del json_data['employeeId']
    if not json_data.get('contractBeginDate') and not json_data.get('contractEndDate'):
        return ParameterException(msg="缺少开始日期或结束日期")
    try:
        data = employee_schema.load(json_data, partial=True)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    if employee.contractEndDate > datetime.date.today():
        return ParameterException(msg="合同未到期，不能续约")
    with db.auto_commit():
        employee.contractBeginDate = data['contractBeginDate']
        employee.contractEndDate = data['contractEndDate']
    OperateLog.write_log(g.user.uid, '员工操作', f'员工{employee.name}续约')
    return Success()