from app.models.base import Base, db
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Enum, Boolean
from marshmallow import Schema, fields, validate


class TrainingProgram(Base):
    __tablename__ = 'training_program'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), index=True)
    content = Column(String(255))
    address = Column(String(64))
    beginDate = Column(Date)
    endDate = Column(Date)
    isEnd = Column(Boolean)


class TrainingProgramSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    content = fields.Str()
    address = fields.Str()
    beginDate = fields.Date()
    endDate = fields.Date()
    isEnd = fields.Boolean()


training_program_schema = TrainingProgramSchema()
training_programs_schema = TrainingProgramSchema(many=True)
