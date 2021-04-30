from flask import Blueprint, current_app, request
from app.api import user
from app.api import employee
from app.api import department
from app.api import job_level
from app.api import training
from app.api import statistics
from app.api import operate_log


def create_blueprint():
    bp = Blueprint('api', __name__)
    user.api.register(bp)
    employee.api.register(bp)
    department.api.register(bp)
    job_level.api.register(bp)
    training.api.register(bp)
    statistics.api.register(bp)
    operate_log.api.register(bp)
    return bp
