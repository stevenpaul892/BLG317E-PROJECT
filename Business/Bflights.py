import sqlite3 as sql
from datetime import datetime

    
def get_dates():
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        query=f""" SELECT DISTINCT scheduled_departure FROM flights"""

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
    

def search_flights(From, Where, Date):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        query=f""" SELECT * FROM flights where departure_airport = '{From}' AND arrival_airport = '{Where}' """

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



