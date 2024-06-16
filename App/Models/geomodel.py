from sqlalchemy import Column
from sqlalchemy import Integer, Column, String
from ..database import Base

from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry


class GeoModel(Base):
    __tablename__ = 'geolocation'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    jenis = Column(String)
    geom = Column(Geometry('POLYGON'))
