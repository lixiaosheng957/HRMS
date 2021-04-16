from app.models.base import Base, db
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Enum, BigInteger, DateTime, Float
from marshmallow import Schema, fields, validate


class BaseConfig(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    coordinateLongitude = Column(Float)
    coordinateLatitude = Column(Float)