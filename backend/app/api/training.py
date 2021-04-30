from flask import current_app, jsonify, g, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.opLog import OperateLog
from app.models.training_program import TrainingProgram, training_program_schema, training_programs_schema
from app.models.employee_training import EmployeeTrainingRecord, employee_training_record_schema, \
    employee_training_records_schema
from app.libs.token_auth import login_required
from app.libs.expection import DatabaseRecordRepeat, FormatError
from app.libs.status_code import Success, ParameterException, DeleteSuccess
from marshmallow import ValidationError
import datetime

api = Redprint('training')


@api.route('/add-training-program', methods=['POST'])
@login_required(['admin', 'hr'])
def add_training_program():
    json_data = request.get_json()
    if not json_data:
        return ParameterException(msg='数据为空')
    training_people_list = json_data['trainingPeople']
    del json_data['trainingPeople']
    try:
        data = training_program_schema.load(json_data)
        if TrainingProgram.query.filter_by(name=data['name'], beginDate=data['beginDate'],
                                           endDate=data['endDate']).first():
            raise DatabaseRecordRepeat(msg='重复的培训项目')
    except ValidationError as err:
        return ParameterException(err.messages)
    except DatabaseRecordRepeat as err:
        return ParameterException(err.msg)
    if data['beginDate'] < datetime.date.today():
        return ParameterException(msg="开始时间错误")
    if data['beginDate'] > data['endDate']:
        return ParameterException(msg="开始时间不能大于结束时间")
    with db.auto_commit():
        training_program = TrainingProgram()
        for key, value in data.items():
            setattr(training_program, key, value)
        training_program.isEnd = False
        training_people = []
        for item in training_people_list:
            employee_training_record = EmployeeTrainingRecord()
            employee_training_record.employeeId = item
            employee_training_record.isFinishAssess = False
            training_people.append(employee_training_record)
        training_program.trainingPeople = training_people
        db.session.add(training_program)
    OperateLog.write_log(g.user.uid, "培训相关操作", "添加培训项目")
    return Success()


@api.route('/publish', methods=['POST'])
@login_required(['admin', 'hr'])
def publish_program():
    program_id = request.get_json()['id']
    if not program_id:
        return ParameterException("未指定项目ID")
    program = TrainingProgram.query.filter_by(id=program_id).first_or_404()
    if program.isPublish:
        return ParameterException("项目已发布")
    elif program.beginDate < datetime.date.today():
        return ParameterException("当前时间已超过项目开始时间，请先修改时间后再发布")
    elif len(program.trainingPeople) == 0:
        return ParameterException("当前培训项目没人参加，请先选择参与者")
    else:
        with db.auto_commit():
            program.isPublish = True
            program.isFinishAssess = False
        OperateLog.write_log(g.user.uid, "培训相关操作", "发布培训项目")
        return Success()


@api.route('/modify-program-base', methods=['POST'])
@login_required(['admin', 'hr'])
def modify_program_base():
    json_data = request.get_json()
    program_id = json_data['programId']
    del json_data['programId']
    if not json_data:
        return ParameterException(msg="数据为空")
    try:
        data = training_program_schema.load(json_data)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    program = TrainingProgram.query.filter_by(id=program_id).first_or_404()
    if program.isPublish:
        return ParameterException(msg="已发布的项目不能修改")
    with db.auto_commit():
        for key, value in data.items():
            setattr(program, key, value)
    OperateLog.write_log(g.user.uid, "培训相关操作", "编辑培训项目基本信息")
    return Success()


@api.route('/modify-training-people', methods=['POST'])
@login_required(['admin', 'hr'])
def modify_training_people():
    json_data = request.get_json()
    if not json_data:
        return ParameterException(msg="数据为空")
    if not json_data.get('id'):
        return ParameterException(msg="项目ID为空")
    for item in json_data['trainingPeople']:
        if not isinstance(item, int):
            return ParameterException(msg="数据格式错误")
    program = TrainingProgram.query.filter_by(id=json_data['id']).first_or_404()
    if program.isPublish:
        return ParameterException(msg="已发布的项目不能修改")
    with db.auto_commit():
        before_training_people = EmployeeTrainingRecord.query.filter_by(trainingProgramId=json_data['id']).all()
        temp_list = [item.employeeId for item in before_training_people]
        no_change = set(temp_list) & set(json_data['trainingPeople'])
        will_delete = list(set(temp_list) - no_change)
        will_add = list(set(json_data['trainingPeople']) - no_change)
        for item in before_training_people:
            if item.employeeId in will_delete:
                db.session.delete(item)
        for item in will_add:
            employee_training_record = EmployeeTrainingRecord()
            employee_training_record.employeeId = item
            employee_training_record.isFinishAssess = False
            db.session.add(employee_training_record)
            program.trainingPeople.append(employee_training_record)
    OperateLog.write_log(g.user.uid, "培训相关操作", "编辑参与人员")
    return Success()


@api.route('/delete-training-program', methods=['POST'])
@login_required(['admin', 'hr'])
def delete_training_program():
    program_id = request.get_json()['programId']
    if not program_id:
        return ParameterException(msg="缺少项目ID")
    program = TrainingProgram.query.filter_by(id=program_id).first_or_404()
    if program.isPublish:
        return ParameterException(msg="已发布的项目不可删除")
    with db.auto_commit():
        program.status = 0
        training_people = EmployeeTrainingRecord.query.filter_by(trainingProgramId=program.id)
        for item in training_people:
            item.status = 0
    OperateLog.write_log(g.user.uid, "培训相关操作", "删除培训项目")
    return DeleteSuccess()


@api.route('/get-program-list')
@login_required(['admin', 'hr'])
def get_training_program_list():
    name = request.args.get('name')
    if name:
        program_list = TrainingProgram.query.filter(TrainingProgram.name.like(f'%{name}%'),
                                                    TrainingProgram.status == 1).all()
    else:
        program_list = TrainingProgram.query.filter_by().all()
    result = training_programs_schema.dump(program_list)
    for item in result:
        start_date = datetime.datetime.strptime(item['beginDate'], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(item['endDate'], '%Y-%m-%d').date()
        if not item['isPublish']:
            item['step'] = '未发布'
        elif start_date <= datetime.date.today() <= end_date and item['isPublish']:
            item['step'] = '进行中'
        elif start_date > datetime.date.today() and item['isPublish']:
            item['step'] = '未开始'
        else:
            item['step'] = '已结束'
    return jsonify(result)


@api.route('/get-program-detail')
def get_program_detail():
    program_id = request.args.get('id')
    just_participant = request.args.get('justParticipant')
    if not program_id:
        return ParameterException('缺少项目ID')
    program = TrainingProgram.query.filter_by(id=program_id).first_or_404()
    if not just_participant:
        result = training_program_schema.dump(program)
        result['participant'] = []
        for item in program.trainingPeople:
            json = {
                'id': item.employee_info.id,
                'name': item.employee_info.name,
                'type': item.employee_info.type,
                'phone': item.employee_info.phone,
                'email': item.employee_info.email,
                'departmentName': item.employee_info.department.name
            }
            result['participant'].append(json)
    else:
        result = [item.employeeId for item in program.trainingPeople]
    return jsonify(result)


@api.route('/get-undone-access-program-list')
@login_required(['admin', 'hr'])
def get_undone_access_program_list():
    program_list = TrainingProgram.query.filter_by(isPublish=True, isEnd=True, isFinishAssess=False).all()
    result = training_programs_schema.dump(program_list)
    for index, item in enumerate(result):
        item['undoneAssessCount'] = 0
        for record in item['trainingPeople']:
            if not record['isFinishAssess']:
                item['undoneAssessCount'] += 1
    return jsonify(result)


@api.route('/get-done-assess-program-list')
@login_required(['admin', 'hr'])
def get_done_assess_program_list():
    program_list = TrainingProgram.query.filter_by(isPublish=True, isEnd=True, isFinishAssess=True).all()
    result = training_programs_schema.dump(program_list)
    return jsonify(result)


@api.route('/get-done-assess-program-detail')
@login_required(['admin', 'hr'])
def get_done_assess_program_detail():
    program_id = request.args.get('id')
    program = TrainingProgram.query.filter_by(id=program_id).first_or_404()
    result = training_program_schema.dump(program)
    result['records'] = []
    for item in program.trainingPeople:
        json = {
            'id': item.id,
            'employeeName': item.employee_info.name,
            'departmentName': item.employee_info.department.name,
            'finishAssessTime': item.finishAssessTime.strftime('%Y-%m-%d %H:%M:%S'),
            'assess': item.assess,
            'level': item.level,
            'isFinish': item.isFinish
        }
        result['records'].append(json)
    return jsonify(result)


@api.route('/get-undone-access-people')
@login_required(['admin', 'hr'])
def get_undone_program_undone_assess_list():
    program_id = request.args.get('id')
    if not program_id:
        return ParameterException(msg="缺少项目ID")
    undone_assess_list = EmployeeTrainingRecord.query.filter_by(trainingProgramId=program_id,
                                                                isFinishAssess=False).all()
    result = employee_training_records_schema.dump(undone_assess_list)
    for index, item in enumerate(result):
        item['employeeName'] = undone_assess_list[index].employee_info.name
        item['employeeDepartment'] = undone_assess_list[index].employee_info.department.name
    return jsonify(result)


@api.route('/assess', methods=['POST'])
@login_required(['admin', 'hr'])
def assess():
    json_data = request.get_json()
    if not json_data:
        return ParameterException(msg="数据为空")
    record_id = json_data.get('id')
    if not record_id:
        return ParameterException(msg="缺少记录ID")
    del json_data['id']
    try:
        data = employee_training_record_schema.load(json_data)
    except ValidationError as err:
        return ParameterException(err.messages)
    record = EmployeeTrainingRecord.query.filter_by(id=record_id).first_or_404()
    if record.isFinishAssess:
        return ParameterException(msg="重复评价")
    with db.auto_commit():
        for key, value in data.items():
            setattr(record, key, value)
        record.isFinishAssess = True
        record.finishAssessTime = datetime.datetime.now()
    undone_finish_assess_list = EmployeeTrainingRecord.query.filter_by(trainingProgramId=record.trainingProgramId,
                                                                       isFinishAssess=False).all()
    if len(undone_finish_assess_list) == 0:
        with db.auto_commit():
            program = TrainingProgram.query.filter_by(id=record.trainingProgramId).first_or_404()
            program.isFinishAssess = True
    OperateLog.write_log(g.user.uid, '培训评价操作', f'对{program.name}参与人 {record.employee_info.name} 作出评价')
    return Success()


@api.route('/get-undone-assess-program-done-assess-people-list')
@login_required(['admin', 'hr'])
def get_undone_assess_program_done_assess_people_list():
    program_id = request.args.get('id')
    if not program_id:
        return ParameterException(msg="缺少项目ID")
    record_list = EmployeeTrainingRecord.query.filter_by(trainingProgramId=program_id, isFinishAssess=True).all()
    result = employee_training_records_schema.dump(record_list)
    for index, item in enumerate(result):
        item['employeeName'] = record_list[index].employee_info.name
        item['employeeDepartment'] = record_list[index].employee_info.department.name
    return jsonify(result)
