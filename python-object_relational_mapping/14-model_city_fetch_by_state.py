#!/usr/bin/python3
"""Script that lists all City objects with their state from hbtn_0e_14_usa"""

from model_state import Base, State
from model_city import City
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sys import argv

if __name__ == "__main__":

    engine = create_engine(
        "mysql+mysqldb://{}:{}@localhost:3306/{}".format(
            argv[1], argv[2], argv[3]
        )
    )

    Session = sessionmaker(bind=engine)
    session = Session()

    results = session.query(State, City).filter(
        State.id == City.state_id
    ).order_by(City.id).all()

    for state, city in results:
        print("{}: ({}) {}".format(state.name, city.id, city.name))

    session.close()
