import sqlite3 as sql
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

    try:
        return albums[0]
    except:
        return None

def check_checkin(ticket_no):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query = """
            SELECT seat_no
            FROM boarding_passes
            WHERE boarding_passes.ticket_no = ?
        """
        cursor.execute(query, (ticket_no,))
        return parse_query_result(cursor.fetchall())

def boarding_pass_checkin(ticket_no):
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
