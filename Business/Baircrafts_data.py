import sqlite3 as sql
import json


def parse_query_result(data):
    albums = []
    for row in data:
        temp = {}
        keys = row.keys()
        print(data)
        for key in keys:
            if key == "model":
                temp[key] = json.loads(row[key])["en"]
            else:
                temp[key] = row[key]
        albums.append(temp)

    return albums


def flight_status_search(ticket_no):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query = """"""

        query += f""" SELECT model """
        query += f""" FROM aircrafts_data, flights, ticket_flights """
        query += f""" WHERE ticket_flights.ticket_no = '{ticket_no}' AND """
        query += f""" ticket_flights.flight_id = flights.flight_id AND """
        query += f""" flights.aircraft_code = aircrafts_data.aircraft_code """

        cursor.execute(query)
        if cursor.fetchall() == []:
            return None
        return parse_query_result(cursor.fetchall())[
            0
        ]  # there will be only one element if there is one
