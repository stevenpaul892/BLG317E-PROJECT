import sqlite3 as sql
import json

def get_cities():
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        query=f""" SELECT airport_code, city FROM airports_data"""

        cursor.execute(query)
        data = cursor.fetchall()
        cities = []

        for row in data:
            temp = [row[0]]    
            parsed_data = json.loads(row[1])
            temp.append(parsed_data['en'])
            cities.append(temp)
            
        return cities
    
def get_dates():
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        query=f""" SELECT airport_code, city FROM airports_data"""

        cursor.execute(query)
        data = cursor.fetchall()
        cities = []

        for row in data:
            temp = [row[0]]    
            parsed_data = json.loads(row[1])
            temp.append(parsed_data['en'])
            cities.append(temp)
            
        return cities

def search_flights(From, Where, Date):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        query=f""" SELECT * FROM flights where departure_airport = '{From}' AND arrival_airport = '{Where}'"""

        cursor.execute(query)
        data = cursor.fetchall()
        flights = []

        for row in data:
            temp = []
            for value in row:
                temp.append(value)
            flights.append(temp)
            
        return flights