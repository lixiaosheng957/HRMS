from sqlalchemy import Column, Table, Integer, ForeignKey, String
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.status_code import AuthFailed
from app.models.base import Base, db
from app.models.role import RoleSchema
from marshmallow import Schema, fields, validate, ValidationError

# User和Role的关联表

roles_users = Table('roles_users',
                    Base.metadata,
                    Column('user_id', Integer, ForeignKey('users.id')),
                    Column('role_id', Integer, ForeignKey('roles.id')))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), unique=True, index=True)
    holder = Column(String(32))
    holderId = Column(Integer, ForeignKey('employee.id'))
    phone = Column(String(11))
    password_hash = Column(String(60))
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'))
    lastLoginTime = db.Column(db.DateTime)  # 上次登录时间
    lastLoginIp = db.Column(db.String(32), nullable=True)  # 上次登录IP
    currentLoginIp = db.Column(db.String(32), nullable=True)  # 当前登录IP
    userRole = roles_users

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def verify(username, password):
        user = User.query.filter_by(username=username).first_or_404()
        if not user.verify_password(password):
            raise AuthFailed(msg="登录验证失败!", error_code=1006)
        role = user.roles
        return {'uid': user.id, 'roles': role}


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True, validate=validate.Length(min=6, max=12))
    password = fields.Str(required=True, validate=validate.Length(min=6), load_only=True)
    holder = fields.Str()
    holderId = fields.Int()
    phone = fields.Str()
    lastLoginTime = fields.TimeDelta()
    lastLoginIp = fields.Str()
    currentLoginIp = fields.Str()
    roles = fields.List(fields.Nested(RoleSchema))


user_schema = UserSchema()
users_schema = UserSchema(many=True, exclude=["currentLoginIp"])
