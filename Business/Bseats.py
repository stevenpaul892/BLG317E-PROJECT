import sqlite3 as sql

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