import sqlite3 as sql
import json


def check_checkin(ticket_no, flightNo):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query = f""" SELECT * FROM boarding_passes WHERE ticket_no = '{ticket_no}' AND flight_id = '{flightNo}'"""

        cursor.execute(query)
        data = cursor.fetchall()
        cities = []
        # ticket no =0005432660784 flight_id =5984
        for row in data:
            temp = {}
            keys = row.keys()
            for key in keys:
                if key == "city":
                    temp[key] = json.loads(row[key])["en"]
                else:
                    temp[key] = row[key]
            cities.append(temp)

        return cities
