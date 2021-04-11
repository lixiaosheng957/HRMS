from app.models.base import Base
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from marshmallow import Schema, fields, validate, ValidationError


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(64))
    redirect = Column(String(64))
    component = Column(String(64))
    name = Column(String(64))
    title = Column(String(64))
    iconCls = Column(String(64))
    keepAlive = Column(Boolean)
    requireAuth = Column(Boolean)
    parentId = Column(Integer, ForeignKey('menus.id'))


class MenuSchema(Schema):
    id = fields.Int()
    path = fields.Str()
    redirect = fields.Str()
    component = fields.Str()
    name = fields.Str()
    title = fields.Str()
    iconCls = fields.Str()
    keepAlive = fields.Boolean()
    requireAuth = fields.Boolean()
    parentId = fields.Int()


menus_schema = MenuSchema(many=True)
