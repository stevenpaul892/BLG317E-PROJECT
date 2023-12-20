import sqlite3 as sql


def check_checkin(ticket_no):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        query=f""" SELECT * FROM boarding_passes WHERE ticket_id = '{ticket_no}'"""

        cursor.execute(query)
        data = cursor.fetchall()
        cities = []

            
        return cities