import sqlite3 as sql
import random

def get_empty_seat(ticket_no):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        query = """"""

        query += f""" SELECT seat_no """
        query += f""" FROM seats, flights, ticket_flights """
        query += f""" WHERE ticket_flights.ticket_no = '{ticket_no}' AND """
        query += f""" ticket_flights.flight_id = flights.flight_id AND """
        query += f""" flights.aircraft_code = seats.aircraft_code """

        cursor.execute(query)

        data = cursor.fetchall()

        taken_seats = []

        for row in data:
            temp = {}
            keys = row.keys()
            for key in keys:
                temp[key] = row[key]
            taken_seats.append(temp)

        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G'] #define letters

        #randomly select a seat
        number = random.randint(1,50)        
        letter = letters[random.randint(0, 6)]

        #randomize till not in taken seats
        while str(number)+letter in taken_seats:
            number = random.randint(1,50)        
            letter = letters[random.randint(0, 6)]

        return str(number)+letter

def Search():
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        query=f""" SELECT * FROM seats"""

        cursor.execute(query)

        data = cursor.fetchall()

        albums = []

        for row in data:
            temp = {}
            keys = row.keys()
            for key in keys:
                temp[key] = row[key]
            albums.append(temp)

        return albums