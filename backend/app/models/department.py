from app.models.base import Base, db
from sqlalchemy import Column, Table, Integer, ForeignKey, String, DateTime, Enum, Boolean
from marshmallow import Schema, fields, validate, ValidationError, pre_dump, post_dump
from marshmallow.utils import is_collection


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), index=True)
    parentId = Column(Integer, ForeignKey('department.id'))
    depPath = Column(String(255))
    enabled = Column(Boolean)
    leader = Column(String(32))
    isParent = Column(Boolean)
    employee = db.relationship('Employee', backref='department', lazy=True)
    jobLevel = db.relationship('JobLevel', backref='department', lazy=True)
    children = db.relationship('Department', back_populates="parent")
    parent = db.relationship('Department', back_populates='children', remote_side=[id])


class DepartmentSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    parentId = fields.Int()
    depPath = fields.Str()
    enabled = fields.Boolean()
    leader = fields.Str()
    # isParent = fields.Boolean()
    children = fields.List(fields.Nested(lambda: DepartmentSchema()))

    def get_attribute(self, obj, key, default):
        if key == 'children':
            return_children = []
            for item in getattr(obj, key):
                if item.status == 1:
                    return_children.append(item)
            return return_children
        else:
            return getattr(obj, key)


department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)
