import sqlite3 as sql
from datetime import datetime


def get_dates():
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query = f""" SELECT DISTINCT scheduled_departure FROM flights"""

        cursor.execute(query)
        data = cursor.fetchall()
        flights = []

        for row in data:
            temp = {}
            keys = row.keys()
            for key in keys:
                temp[key] = row[key]
            flights.append(temp)

        return flights


import sqlite3 as sql


def search_flights(From, Where, When):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        # Construct the query with string formatting, which is not recommended due to the risk of SQL injection
        query = f"""SELECT * FROM flights 
                    WHERE departure_airport = '{From}' 
                    AND arrival_airport = '{Where}' 
                    AND scheduled_departure > '{When}'"""

        # Execute the query
        cursor.execute(query)
        data = cursor.fetchall()
        flights = []

        for row in data:
            temp = {}
            keys = row.keys()
            for key in keys:
                temp[key] = row[key]
            flights.append(temp)

        print(flights)
        return flights


def get_flight_info_from_flight_id(flight_id):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query = f""" SELECT * FROM flights where flight_id = '{flight_id}' """

        cursor.execute(query)
        data = cursor.fetchall()
        flights = []

        for row in data:
            temp = {}
            keys = row.keys()
            for key in keys:
                temp[key] = row[key]
            flights.append(temp)

        return flights[0]  # there will be only one match if there is one
