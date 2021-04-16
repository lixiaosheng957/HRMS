from flask import Blueprint
from app.api import user
from app.api import employee
from app.api import department
from app.api import job_level
from app.api import base_config


def create_blueprint():
    bp = Blueprint('api', __name__)
    user.api.register(bp)
    employee.api.register(bp)
    department.api.register(bp)
    job_level.api.register(bp)
    base_config.api.register(bp)
    return bp
