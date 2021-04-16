from app.models.base import Base, db
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Enum
from marshmallow import Schema, fields, validate
from flask import g


class OperateLog(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    operatorId = Column(Integer, ForeignKey('users.id'))
    operateType = Column(String(32))
    operateContent = Column(String(256))

    @staticmethod
    def write_log(operatorId, operateType, operateContent):
        with db.auto_commit():
            operate_log = OperateLog()
            operate_log.operatorId = operatorId
            operate_log.operateType = operateType
            operate_log.operateContent = operateContent
            db.session.add(operate_log)