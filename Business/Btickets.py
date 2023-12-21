import sqlite3 as sql
import json


def flight_status_search():
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query = f""" SELECT * FROM tickets LIMIT 5"""

        cursor.execute(query)

        data = cursor.fetchall()

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
