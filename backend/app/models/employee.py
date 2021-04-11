from app.models.base import Base
from sqlalchemy import Column, Table, Integer, ForeignKey, String, Date, Enum, Float
from marshmallow import Schema, fields, validate, ValidationError
from app.models.department import Department


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    gender = Column(Enum('男', '女'))
    name = Column(String(32), index=True)
    nation = Column(String(32))
    nativePlace = Column(String(32))
    birthday = Column(Date())
    idCard = Column(String(18), unique=True)
    email = Column(String(32))
    wedlock = Column(Enum('已婚', '未婚', '离异'))
    phone = Column(String(11))
    workAge = Column(Float)
    tipTopDegree = Column(Enum(
        '博士', '硕士', '本科', '大专', '高中', '初中', '小学', '其他'))
    school = Column(String(32))
    specialty = Column(String(32))
    workState = Column(Enum('在职', '离职'))
    type = Column(Enum('正式员工', '试用员工', '实习员工'))
    departmentId = Column(Integer, ForeignKey('department.id'))
    jobLevelId = Column(Integer, ForeignKey('job_level.id'))
    noWorkDate = Column(Date())
    beginDate = Column(Date())
    endDate = Column(Date())


class EmployeeSchema(Schema):
    id = fields.Int()
    gender = fields.Str(required=True, validate=validate.OneOf(['男', '女']))
    name = fields.Str(required=True)
    nation = fields.Str()
    nativePlace = fields.Str()
    birthday = fields.Date()
    idCard = fields.Str(required=True, validate=validate.Length(min=18, max=18))
    email = fields.Str()
    wedlock = fields.Str(validate=validate.OneOf(['已婚', '未婚', '离异']))
    phone = fields.Str(validate=validate.Length(min=11, max=11))
    workAge = fields.Float()
    tipTopDegree = fields.Str(validate=validate.OneOf(
        ['博士', '硕士', '本科', '大专', '高中', '初中', '小学', '其他']))
    school = fields.Str()
    specialty = fields.Str()
    type = fields.Str(validate=validate.OneOf(['正式员工', '试用员工', '实习员工']))
    workState = fields.Str(validate=validate.OneOf(['在职', '离职']))
    departmentId = fields.Int()
    jobLevelId = fields.Int()
    noWorkDate = fields.Date()
    beginDate = fields.Date()
    endDate = fields.Date()


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
