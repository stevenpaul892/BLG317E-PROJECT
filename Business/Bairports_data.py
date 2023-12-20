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
            temp = {}
            keys = row.keys()
            for key in keys:
                if key == 'city':
                    temp[key] = json.loads(row[key])['en']
                else:
                    temp[key] = row[key]
            cities.append(temp)
            
        return cities