from app.models.base import Base, db
from sqlalchemy import Column, Table, Integer, ForeignKey, String, DateTime, Enum, Boolean
from marshmallow import Schema, fields, validate, ValidationError


class JobLevel(Base):
    __tablename__ = 'job_level'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    titleLevel = Column(Enum('实习', '高级', '中级', '初级', '管理层'))
    enabled = Column(Boolean)
    departmentId = Column(Integer, ForeignKey('department.id'))
    employee = db.relationship('Employee', backref='job_level', lazy=True)


class JobLevelSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    titleLevel = fields.Str(validate=validate.OneOf(['实习', '高级', '中级', '初级', '管理层']))
    enabled = fields.Boolean()
    departmentId = fields.Int()


job_level_schema = JobLevelSchema()
job_levels_schema = JobLevelSchema(many=True)
