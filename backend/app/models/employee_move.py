from app.models.base import Base, db
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Enum, Float
from marshmallow import Schema, fields, validate


class EmployeeMoveRecord(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    employeeId = Column(Integer, ForeignKey('employee.id'))
    reason = Column(String(255))
    moveTime = Column(Date)
    workTime = Column(String(32))


class EmployeeMoveRecordSchema(Schema):
    id = fields.Int()
    employeeId = fields.Int()
    reason = fields.Str()
    moveTime = fields.Date()
    workTime = fields.Str()


employee_move_record_schema = EmployeeMoveRecordSchema()
employee_move_records_schema = EmployeeMoveRecordSchema(many=True)
