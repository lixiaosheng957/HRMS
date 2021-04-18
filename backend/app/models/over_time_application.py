from app.models.base import Base, db
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Enum, Boolean, DateTime
from marshmallow import Schema, fields, validate
from app.models.employee_training import EmployeeTrainingRecordSchema


class OverTimeApplication(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    employeeId = Column(Integer, ForeignKey('employee.id'))
    beginTime = Column(DateTime)
    endTime = Column(DateTime)
    approvedBy = Column(Integer, ForeignKey('users.id'))
    reason = Column(String(128))
    approveStatus = Column(Enum('未审批', '通过', '不通过'))
    approveTime = Column(DateTime)
    option = Column(String(128))


class OverTimeApplicationSchema(Schema):
    id = fields.Int()
    employeeId = fields.Int()
    beginTime = fields.DateTime()
    endTime = fields.DateTime()
    approvedBy = fields.Int()
    reason = fields.Str()
    approveStatus = fields.Str(validate=validate.OneOf(['未审批', '通过', '不通过']))
    approveTime = fields.DateTime()
    option = fields.Str()


overtime_application_schema = OverTimeApplicationSchema()
overtime_applications_schema = OverTimeApplicationSchema(many=True)
