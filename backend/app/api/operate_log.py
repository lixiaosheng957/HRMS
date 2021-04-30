from flask import current_app, jsonify, g, request
from app.libs.redprint import Redprint
from app.models.opLog import OperateLog
from app.libs.token_auth import login_required
from app.libs.status_code import ParameterException
from datetime import datetime
from sqlalchemy import and_

api = Redprint('operate-log')


@api.route('/get-my-operate-log')
@login_required(['admin', 'hr'])
def get_operate_log():
    page = request.args.get('page')
    page_size = request.args.get('pageSize')
    operate_type = request.args.get('type')
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')
    if not page or not page_size:
        return ParameterException(msg="缺少分页信息")
    try:
        page = int(page)
        page_size = int(page_size)
    except ValueError:
        return ParameterException("当前页或页数格式错误")
    user_id = g.user.uid
    if operate_type and not start_time and not end_time:
        operate_log_list_pagination = OperateLog.query.filter(OperateLog.operateType.like(f'%{operate_type}%'),
                                                              OperateLog.operatorId == user_id,
                                                              OperateLog.status == 1).paginate(
            page, per_page=page_size, error_out=False)
    elif start_time and end_time and not operate_type:
        operate_log_list_pagination = OperateLog.query.filter(
            and_(OperateLog.create_time >= time_str2timestamp(start_time),
                 OperateLog.create_time <= time_str2timestamp(end_time),
                 OperateLog.status == 1)).paginate(
            page, per_page=page_size, error_out=False)
    elif operate_type and start_time and end_time:
        operate_log_list_pagination = OperateLog.query.filter(
            and_(OperateLog.create_time >= time_str2timestamp(start_time),
                 OperateLog.create_time <= time_str2timestamp(end_time),
                 OperateLog.operateType.like(f'%{operate_type}%'),
                 OperateLog.status == 1)).paginate(
            page, per_page=page_size, error_out=False)
    else:
        operate_log_list_pagination = OperateLog.query.filter_by().paginate(
            page, per_page=page_size, error_out=False)
    result = {'data': []}
    for record in operate_log_list_pagination.items:
        json = {
            'id': record.id,
            'type': record.operateType,
            'content': record.operateContent,
            'time': record.create_datetime.strftime('%Y-%m-%d %H:%M:%S')
        }
        result['data'].append(json)
    result['total'] = operate_log_list_pagination.total
    return jsonify(result)


@api.route('/get-all-operate-log')
@login_required(['admin'])
def get_all_operate_log():
    page = request.args.get('page')
    page_size = request.args.get('pageSize')
    params = []
    if not page or not page_size:
        return ParameterException(msg="缺少分页信息")
    try:
        page = int(page)
        page_size = int(page_size)
    except ValueError:
        return ParameterException("当前页或页数格式错误")
    if request.args.get('type'):
        operate_type = request.args.get('type')
        params.append(OperateLog.operateType.like(f'%{operate_type}%'))
    if request.args.get('startTime') and request.args.get('endTime'):
        start_time = request.args.get('startTime')
        end_time = request.args.get('endTime')
        params.append(OperateLog.create_time >= time_str2timestamp(start_time))
        params.append(OperateLog.create_time <= time_str2timestamp(end_time))
    if request.args.get('operator'):
        operator_id = request.args.get('operator')
        params.append(OperateLog.operatorId == operator_id)
    params.append(OperateLog.status == 1)
    operate_log_list_pagination = OperateLog.query.filter(*params).paginate(
        page, per_page=page_size, error_out=False)
    result = {'data': []}
    for record in operate_log_list_pagination.items:
        json = {
            'id': record.id,
            'operateAccount': record.user.username,
            'type': record.operateType,
            'content': record.operateContent,
            'time': record.create_datetime.strftime('%Y-%m-%d %H:%M:%S')
        }
        if not record.user.holderId:
            json['accountHolder'] = record.user.holder + '(管理员)'
        else:
            json['accountHolder'] = record.user.holder_info.name
        result['data'].append(json)
    result['total'] = operate_log_list_pagination.total
    return jsonify(result)


def time_str2timestamp(time_str):
    c_day = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    return int(c_day.timestamp())
