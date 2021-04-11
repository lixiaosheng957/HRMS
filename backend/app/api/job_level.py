from flask import current_app, jsonify, g, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.job_level import JobLevel, job_level_schema, job_levels_schema
from app.libs.token_auth import login_required
from app.libs.status_code import Success, ParameterException, DeleteSuccess
from marshmallow import ValidationError
from sqlalchemy import and_, or_

api = Redprint('job-level')


@api.route('/add', methods=['POST'])
@login_required(['admin'])
def add_job_level():
    json_data = request.get_json()
    if not json_data:
        return ParameterException()
    try:
        data = job_level_schema.load(json_data)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    job_level = JobLevel.query.filter(JobLevel.name == data['name']).first()
    if job_level and job_level.status:
        return ParameterException(msg="重复职位!")
    elif job_level and job_level.status == 0:
        with db.auto_commit():
            for key, value in data.items():
                setattr(job_level, key, value)
                job_level.status = 1
                db.session.add(job_level)
    else:
        with db.auto_commit():
            job_level = JobLevel()
            for key, value in data.items():
                setattr(job_level, key, value)
                db.session.add(job_level)
    return Success()


@api.route('/modify')
@login_required(['admin'])
def modify_job_level():
    json_data = request.get_json()
    if not json_data:
        return ParameterException()
    try:
        data = job_level_schema.load(json_data)
    except ValidationError as err:
        return ParameterException(msg=err.messages)
    job_level = JobLevel.query.filter_by(id=data['id']).first_or_404()
    with db.auto_commit():
        for key, value in data.items():
            setattr(job_level, key, value)
    return Success()


@api.route('/delete')
@login_required(['admin'])
def delete_job_level():
    job_level_id = request.get_json()['id']
    if not job_level_id:
        return ParameterException()
    job_level = JobLevel.query.filter_by(id=job_level_id).fitst_or_404()

    if len(job_level.employee) > 0:
        return ParameterException(msg="删除失败，该职位员工数量不为零！")

    with db.auto_commit():
        job_level.status = 0
    return DeleteSuccess()


@api.route('/get-job-level-list')
@login_required(['admin'])
def get_job_level_list():
    name = request.args.get('name')
    department_id = None
    if request.args.get('departmentId'):
        department_id = int(request.args.get('departmentId'))
    if name and department_id:
        if request.args.get('tags'):
            job_level_list = JobLevel.query.filter(
                and_(JobLevel.name.like(f'%{name}%'), JobLevel.departmentId == department_id),
                JobLevel.status == 1).all()
            job_level_select = []
            for item in job_level_list:
                json = {'value': item.id, 'label': item.name}
                job_level_select.append(json)
            return jsonify(job_level_select)
        else:
            job_level_list = JobLevel.query.filter(
                and_(JobLevel.name.like(f'%{name}%'), JobLevel.departmentId == department_id),
                JobLevel.status == 1).all()
    elif department_id or name:
        job_level_list = JobLevel.query.filter(
            or_(and_(JobLevel.name.like(f'%{name}%'), JobLevel.status == 1),
                and_(JobLevel.departmentId == department_id, JobLevel.status == 1))).all()
    else:
        job_level_list = JobLevel.query.filter_by().all()
    result = job_levels_schema.dump(job_level_list)
    for index, item in enumerate(result):
        item['number'] = len(job_level_list[index].employee)
    return jsonify(result)
