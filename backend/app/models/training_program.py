from app.models.base import Base, db
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Enum, Boolean
from marshmallow import Schema, fields, validate
from app.models.employee_training import EmployeeTrainingRecordSchema


class TrainingProgram(Base):
    __tablename__ = 'training_program'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), index=True)
    content = Column(String(255))
    address = Column(String(64))
    beginDate = Column(Date)
    endDate = Column(Date)
    isPublish = Column(Boolean)
    isEnd = Column(Boolean)
    isFinishAssess = Column(Boolean)
    trainingPeople = db.relationship('EmployeeTrainingRecord', backref='training_program', lazy=True)


class TrainingProgramSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    content = fields.Str(required=True)
    address = fields.Str(required=True)
    beginDate = fields.Date(required=True)
    endDate = fields.Date(required=True)
    isPublish = fields.Boolean()
    isEnd = fields.Boolean()
    isFinishAssess = fields.Boolean()
    trainingPeople = fields.List(fields.Nested(EmployeeTrainingRecordSchema))


training_program_schema = TrainingProgramSchema()
training_programs_schema = TrainingProgramSchema(many=True)
