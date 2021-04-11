from app.models.base import Base, db
from sqlalchemy import Column, Table, Integer, ForeignKey, String
from marshmallow import Schema, fields, validate, ValidationError
from app.models.menu import Menu

role_menu = Table('role_menu',
                  Base.metadata,
                  Column('role_id', Integer, ForeignKey('roles.id')),
                  Column('menu_id', Integer, ForeignKey('menus.id')))


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    menus = db.relationship('Menu', secondary=role_menu, backref=db.backref('roles', lazy='dynamic'))
    roleMenu = role_menu

    def __repr__(self):
        return '<Role %r>' % self.name


class RoleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
