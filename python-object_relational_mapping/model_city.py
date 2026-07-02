#!/usr/bin/python3
"""Module that maps the cities table in the SQL"""
from sqlalchemy import Integer, String, Column, ForeignKey
from model_state import Base, State


class City(Base):
    """Class for the cities table in the SQL"""
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
    state_id = Column(Integer, ForeignKey(State.id), nullable=False)
