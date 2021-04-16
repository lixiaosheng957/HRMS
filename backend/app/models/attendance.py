from app.models.base import Base, db
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Enum, BigInteger, DateTime
from marshmallow import Schema, fields, validate


class AttendanceRecord(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    employeeId = Column(Integer, ForeignKey('employee.id'))
    startTimeAm = Column(DateTime)
    endTimeAm = Column(DateTime)
    startTimePm = Column(DateTime)
    endTimePm = Column(DateTime)
    month = Column(Integer)


class AttendanceRecordSchema(Schema):
    id = fields.Int()
    employeeId = fields.Int()
    startTimeAm = fields.DateTime()
    endTimeAm = fields.DateTime()
    startTimePm = fields.DateTime()
    endTimePm = fields.DateTime()
    month = fields.Int()