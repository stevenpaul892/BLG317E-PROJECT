import sqlite3 as sql

def Search():
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        query=f""" SELECT * FROM aircrafts_data"""

        cursor.execute(query)

        data = cursor.fetchall()

        albums = []

        for row in data:
            temp = []
            for value in row:
                temp.append(value)
            albums.append(temp)

        return albums