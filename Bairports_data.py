import sqlite3 as sql
import json

def get_cities():
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        query=f""" SELECT *  FROM airports_data"""

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
    pass

def search_flights():
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        query=f"""  SELECT *  FROM tickets"""

        cursor.execute(query)
        data = cursor.fetchall()
        flights = []

        for row in data:
            temp = []
            for value in row:
                temp.append(value)
            flights.append(temp)
        print(flights)
        return flights


search_flights()