#!/usr/bin/python3

from sqlalchemy import Integer, String, Column, ForeignKey
from model_state import Base, State

class City(Base):
    
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
    state_id = Column(Integer, ForeignKey(State.id), nullable=False)
