from wtforms import StringField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, length, Regexp
from wtforms import ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseFrom as Form


class ClientForm(Form):
    username = StringField(validators=[DataRequired(message='不允许为空'), length(min=6, max=12)])
    secret = StringField(validators=[DataRequired(message='不允许为空'), length(min=6)])
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError:
            raise ValueError
        self.type.data = client


class UserForm(Form):
    username = StringField(validators=[DataRequired(message='不允许为空'), length(min=6, max=12)])
    secret = StringField(validators=[DataRequired(message='不允许为空'), length(min=6)])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])
