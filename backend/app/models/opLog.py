from app.models.base import Base, db
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Enum
from marshmallow import Schema, fields, validate


class OperateLog(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    operatorId = Column(Integer, ForeignKey('user.id'))
    operateType = Column(String(32))
    operateContent = Column(String(256))
