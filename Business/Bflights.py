import sqlite3 as sql
import datetime
import json


def parse_query_result(data):
    albums = []
    for row in data:
        temp = {}
        keys = row.keys()

        for key in keys:
            if key == "model":
                temp[key] = json.loads(row[key])["en"]
            else:
                temp[key] = row[key]
        albums.append(temp)

    return albums


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
        year, month, day = When.split('-')
        When_offset = datetime.datetime(year=int(year), month=int(month), day=int(day))
        When_offset += datetime.timedelta(hours=24)

        # Construct the query with string formatting, which is not recommended due to the risk of SQL injection
        query = f"""SELECT * FROM flights 
                    WHERE departure_airport = '{From}' 
                    AND arrival_airport = '{Where}' 
                    AND scheduled_departure > '{When}'
                    AND scheduled_departure < '{When_offset}'
                    AND status = 'Scheduled'
                    ORDER BY scheduled_departure ASC"""

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

        return flights[0]


def flight_status_search(ticket_no):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query = """
            SELECT scheduled_departure, departure_airport, arrival_airport
            FROM flights
            JOIN ticket_flights ON ticket_flights.flight_id = flights.flight_id
            WHERE ticket_flights.ticket_no = ?
        """

        cursor.execute(query, (ticket_no,))
        try:
            return parse_query_result(cursor.fetchall())[0]
        except:
            return None