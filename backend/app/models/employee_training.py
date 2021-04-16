from app.models.base import Base, db
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Enum, Boolean
from marshmallow import Schema, fields, validate


class EmployeeTrainingRecord(Base):
    __tablename__ = 'employee_training_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employeeId = Column(Integer, ForeignKey('employee.id'))
    trainingProgramId = Column(Integer, ForeignKey('training_program.id'))
    assess = Column(String(255))
    level = Column(Enum('优秀', '良好', '中等', '较差'))
    isFinish = Column(Boolean)


class EmployeeTrainingRecordSchema(Schema):
    id = fields.Int()
    employeeId = fields.Int()
    trainingProgramId = fields.Int()
    assess = fields.Str()
    level = fields.Str(validate=validate.OneOf(['优秀', '良好', '中等', '较差']))
    isFinish = fields.Boolean()


employee_training_record_schema = EmployeeTrainingRecordSchema()
employee_training_records_schema = EmployeeTrainingRecordSchema(many=True)