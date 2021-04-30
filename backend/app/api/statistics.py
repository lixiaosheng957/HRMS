from flask import jsonify
from app.libs.redprint import Redprint
from app.models.department import Department
from app.models.employee import Employee, employees_schema
from app.models.employee_transfer import EmployeeTransfer
from app.models.opLog import OperateLog
from app.models.employee_move import EmployeeMoveRecord
from app.models.training_program import TrainingProgram, training_programs_schema
from app.models.employee_training import EmployeeTrainingRecord
from app.libs.token_auth import login_required
import datetime
import calendar

api = Redprint('statistics')


@api.route('/employee-type-statistics')
@login_required(['admin', 'hr'])
def employee_type_statistics():
    full_time_employees = Employee.query.filter_by(type="正式员工", workState="在职").all()
    probation_period_employees = Employee.query.filter_by(type="试用员工", workState="在职").all()
    internship_employees = Employee.query.filter_by(type="实习员工", workState="在职").all()
    leave_employees = Employee.query.filter_by(workState="离职").all()
    result = {
        'fullTimeEmployees': len(full_time_employees),
        'probationPeriodEmployees': len(probation_period_employees),
        'internshipEmployees': len(internship_employees),
        'leaveEmployees': len(leave_employees)
    }
    return jsonify(result)


@api.route('/department-employee-statistics')
@login_required(['admin', 'hr'])
def department_employee_statistics():
    departments = Department.query.filter_by().all()
    result = {
        'departmentNameArray': [],
        'fullTimeEmployees': [],
        'probationPeriodEmployees': [],
        'internshipEmployees': []
    }
    for item in departments:
        result['departmentNameArray'].append(item.name)
        if len(item.employee) > 0:
            full_time_employees_count = 0
            probation_period_employees_count = 0
            internship_employees_count = 0
            for employee in item.employee:
                if employee.status and employee.workState == "在职":
                    if employee.type == "正式员工":
                        full_time_employees_count += 1
                    elif employee.type == "试用员工":
                        probation_period_employees_count += 1
                    else:
                        internship_employees_count += 1
            result['fullTimeEmployees'].append(full_time_employees_count)
            result['probationPeriodEmployees'].append(probation_period_employees_count)
            result['internshipEmployees'].append(internship_employees_count)
        else:
            result['fullTimeEmployees'].append(0)
            result['probationPeriodEmployees'].append(0)
            result['internshipEmployees'].append(0)

    return jsonify(result)


@api.route('/personnel-info-statistics')
@login_required(['admin', 'hr'])
def personnel_info_statistics():
    first_day, last_day = getMonthFirstDayAndLastDay()
    first_day_datetime_timestamp = int(datetime.datetime(first_day.year, first_day.month, first_day.day).timestamp())
    last_day_datetime_first_day_datetime_timestamp = int(
        datetime.datetime(last_day.year, last_day.month, last_day.day, 23, 59, 59).timestamp())
    join = Employee.query.filter(Employee.joinDate.between(first_day, last_day), Employee.status == 1).count()
    transfer = EmployeeTransfer.query.filter(EmployeeTransfer.transferTime.between(first_day, last_day),
                                             EmployeeTransfer.status == 1).count()
    renew = OperateLog.query.filter(
        OperateLog.create_time >= first_day_datetime_timestamp,
        OperateLog.create_time <= last_day_datetime_first_day_datetime_timestamp,
        OperateLog.operateContent.like('%续约%'), OperateLog.status == 1).count()
    move = EmployeeMoveRecord.query.filter(EmployeeMoveRecord.moveTime.between(first_day, last_day),
                                           EmployeeMoveRecord.status == 1).count()
    result = {
        'join': join,
        'transfer': transfer,
        'renew': renew,
        'move': move
    }
    return jsonify(result)


@api.route('/to-be-renew')
@login_required(['admin', 'hr'])
def to_be_renew():
    now_day = datetime.date.today()
    to_be_renew_list = Employee.query.filter(
        Employee.contractEndDate.between(now_day, now_day + datetime.timedelta(days=5)),
        Employee.workState == "在职",
        Employee.status == 1
    )
    result = employees_schema.dump(to_be_renew_list)
    for index, item in enumerate(result):
        item['departmentName'] = to_be_renew_list[index].department.name
    return jsonify(result)


@api.route('/contract-end')
@login_required(['admin', 'hr'])
def contract_end():
    today = datetime.date.today()
    contract_end_list = Employee.query.filter(
        Employee.contractEndDate < today,
        Employee.workState == "在职",
        Employee.status == 1
    )
    result = employees_schema.dump(contract_end_list)
    for index, item in enumerate(result):
        item['departmentName'] = contract_end_list[index].department.name
    return jsonify(result)


@api.route('/undone-training-program')
@login_required(['admin', 'hr'])
def get_undone_training_program():
    undone_list = TrainingProgram.query.filter_by(isFinishAssess=False, isEnd=True).all()
    result = training_programs_schema.dump(undone_list)
    for index, item in enumerate(result):
        count = EmployeeTrainingRecord.query.filter_by(isFinishAssess=False, trainingProgramId=item['id']).count()
        item['undoneCount'] = count
    return jsonify(result)


def getMonthFirstDayAndLastDay(year=None, month=None):
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    # 获取当月第一天的星期和当月的总天数
    first_day_week_day, month_range = calendar.monthrange(year, month)

    # 获取当月的第一天
    first_day = datetime.date(year=year, month=month, day=1)
    last_day = datetime.date(year=year, month=month, day=month_range)

    return first_day, last_day