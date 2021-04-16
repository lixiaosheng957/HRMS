from flask import current_app, jsonify, g, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.libs.token_auth import login_required
from app.libs.status_code import Success, ParameterException, DeleteSuccess
from marshmallow import ValidationError

api = Redprint('attendance')
