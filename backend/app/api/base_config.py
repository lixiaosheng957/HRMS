from flask import current_app, jsonify, g, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.base_config import BaseConfig
from app.libs.token_auth import login_required
from app.libs.status_code import Success, ParameterException, DeleteSuccess
from marshmallow import ValidationError
import requests

api = Redprint('base-config')


@api.route('/coordinate',methods=['POST'])
@login_required(['admin'])
def set_coordinate():
    json_data = request.get_json()
    if not json_data:
        return ParameterException()
    location = json_data['location']
    params = {'address': location, 'key': 'VUOBZ-JGEKG-X6OQU-IH2WM-A3OEE-GHBND'}
    r = requests.get('https://apis.map.qq.com/ws/geocoder/v1/', params=params)
    result = r.json()
    return r.json()
