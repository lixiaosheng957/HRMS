from app.models.base import Base
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Enum, Boolean, DateTime
from marshmallow import Schema, fields, validate


class EmployeeTransfer(Base):
    __tablename__ = 'employee_transfer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employeeId = Column(Integer, ForeignKey('employee.id'))
    transferType = Column(Enum('职位变动', '试用期转正', '实习转试用'))
    type = Column(Enum('主动申请', '上级要求'))
    operatorId = Column(Integer, ForeignKey('users.id'))
    transferTime = Column(Date)
    transferDepartmentId = Column(Integer, ForeignKey('department.id'))
    transferJobId = Column(Integer, ForeignKey('job_level.id'))
    contractBeginDate = Column(Date)
    contractEndDate = Column(Date)
    beforeTransferDepartmentId = Column(Integer, ForeignKey('department.id'))
    beforeTransferJobId = Column(Integer, ForeignKey('job_level.id'))
    beforeContractBeginDate = Column(Date)
    beforeContractEndDate = Column(Date)
    tips = Column(String(255))


class EmployeeSchema(Schema):
    id = fields.Int()
    employeeId = fields.Int(required=True)
    transferType = fields.Str(required=True, validate=validate.OneOf(['职位变动', '试用期转正', '实习转试用']))
    type = fields.Str(required=True, validate=validate.OneOf(['主动申请', '上级要求']))
    operatorId = fields.Int()
    transferTime = fields.Date()
    transferDepartmentId = fields.Int()
    transferJobId = fields.Int()
    contractBeginDate = fields.Date()
    contractEndDate = fields.Date()
    beforeTransferDepartmentId = fields.Int()
    beforeTransferJobId = fields.Int()
    beforeContractBeginDate = fields.Date()
    beforeContractEndDate = fields.Date()
    tips = fields.Str()


employee_transfer_schema = EmployeeSchema()
employee_transfers_schema = EmployeeSchema(many=True)
