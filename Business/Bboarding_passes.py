import sqlite3 as sql
import json


def check_checkin(ticket_no):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query = f""" SELECT * FROM boarding_passes WHERE ticket_no = '{ticket_no}'"""

        cursor.execute(query)
        data = cursor.fetchall()
        cities = []
        
        for row in data:
            temp = {}
            keys = row.keys()
            for key in keys:
                temp[key] = row[key]
            cities.append(temp)

        print(cities)
        print(len(cities) != 0)

        return len(cities) != 0

def insert_boardinpass(ticket_no, flight_id, boarding_no, seat_no):
     with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query = f""" INSERT INTO boarding_passes(ticket_no, flight_id, boarding_no, seat_no) """
        query +=f""" VALUES ('{ticket_no}', {flight_id}, {boarding_no}, '{seat_no}')"""

        try:
            cursor.execute(query)
            return True
        except:
            return False