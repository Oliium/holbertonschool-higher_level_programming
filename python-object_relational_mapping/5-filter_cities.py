#!/usr/bin/python3
"""Script that lists all cities of a given state from hbtn_0e_4_usa"""

import MySQLdb
from sys import argv

if __name__ == "__main__":

    db = MySQLdb.connect(
        host="localhost",
        port=3306,
        user=argv[1],
        passwd=argv[2],
        db=argv[3],
    )

    cur = db.cursor()
    cur.execute(
        "SELECT cities.name FROM cities "
        "JOIN states ON cities.state_id = states.id "
        "WHERE states.name = %s "
        "ORDER BY cities.id ASC",
        (argv[4],)
    )

    rows = cur.fetchall()
    print(", ".join([row[0] for row in rows]))
