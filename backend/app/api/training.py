from flask import current_app, jsonify, g, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.training_program import TrainingProgram, training_program_schema, training_programs_schema
from app.libs.token_auth import login_required
from app.libs.expection import DatabaseRecordRepeat
from app.libs.status_code import Success, ParameterException, DeleteSuccess
from marshmallow import ValidationError

api = Redprint('training')


@api.route('/add-training-program', methods=['POST'])
@login_required(['admin', 'hr'])
def add_training_program():
    json_data = request.get_json()
    if not json_data:
        return ParameterException(msg='数据为空')
    try:
        data = training_program_schema.load(json_data)
        if TrainingProgram.query.filter_by(name=data['name'], beginDate=data['beginDate'], endDate=data['endDate']):
            raise DatabaseRecordRepeat(msg='重复的培训项目')
    except ValidationError as err:
        return ParameterException(err.messages)
    except DatabaseRecordRepeat as err:
        return ParameterException(err.msg)
    with db.auto_commit():
        training_program = TrainingProgram()
        for key, value in data.items():
            setattr(training_program, key, value)
    return Success()


@api.route('/delete-training-program', methods=['POST'])
@login_required(['admin', 'hr'])
def delete_training_program():
    program_id = request.get_json()['programId']
    if not program_id:
        return ParameterException(msg="缺少项目ID")
    program = TrainingProgram.query.filter_by(id=program_id).first_or_404()
    with db.auto_commit():
        program.status = 0
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
    return jsonify(result)


@api.route('/get-program-detail')
def get_program_detail():
    program_id = request.args.get('id')
    if not program_id:
        return ParameterException('缺少项目ID')
    program = TrainingProgram.query.filter_by(id=program_id).first_or_404()
    result = training_program_schema.dump(program)
    return jsonify(result)
