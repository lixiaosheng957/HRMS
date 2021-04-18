from flask import current_app, jsonify, g, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.opLog import OperateLog
from app.models.over_time_application import OverTimeApplication, overtime_application_schema, \
    overtime_applications_schema
from app.models.employee import Employee
from app.libs.token_auth import login_required
from app.libs.expection import DatabaseRecordRepeat
from app.libs.status_code import Success, ParameterException, DeleteSuccess
from marshmallow import ValidationError

api = Redprint('application')


@api.route('/create-overtime-application', methods=['POST'])
@login_required(['admin', 'employee'])
def create_overtime_application():
    json_data = request.get_json()
    if not json_data:
        return ParameterException('数据为空')
    try:
        data = overtime_application_schema.load(json_data)
        if OverTimeApplication.query.filter_by(beginTime=data['beginTime'], endTime=data['endTime']):
            raise DatabaseRecordRepeat(msg='已存在相同时间段的申请')
    except ValidationError as err:
        return ParameterException(err.messages)
    except DatabaseRecordRepeat as err:
        return ParameterException(err.msg)

    with db.auto_commit():
        application = OverTimeApplication()
        for key, value in data.items():
            setattr(application, key, value)
        db.session.add(application)
    OperateLog.write_log(g.user.uid, "申请操作", "发起加班申请")
    return Success()


@api.route('/get-overtime-application-list')
@login_required(['admin', 'hr', 'employee'])
def get_overtime_application_list():
    status = request.args.get('status')
    if 'employee' in g.user.roles and len(g.user.roles) == 1:
        application_list = OverTimeApplication.query.filter_by(employeeId=g.user.holder_id, approveStatus=status).all()
    elif 'hr' in g.user.roles:
        application_list = OverTimeApplication.query.filter_by(approvedBy=g.user.holer_id, approveStatus=status).all()
    else:
        application_list = OverTimeApplication.query.filter_by(approveStatus=status).all()
    result = overtime_applications_schema.dump(application_list)
    for index, item in enumerate(result):
        item['employeeName'] = Employee.query.filter(Employee.id == item['employeeId']).first().name
        item['approveName'] = Employee.query.filter(Employee.id == g.user.holer_id).first()
    return jsonify(result)
