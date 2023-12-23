import sqlite3 as sql

def search_ticket_price(flight_id):
    with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        query=f""" SELECT amount, fare_conditions FROM ticket_flights where flight_id = '{flight_id}' """

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

def get_flight_from_ticket(ticket_no):
     with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        query=f""" SELECT * FROM ticket_flights where ticket_no = '{ticket_no}' """

        cursor.execute(query)
        data = cursor.fetchall()
        flights = []

        for row in data:
            temp = {}
            keys = row.keys()
            for key in keys:
                temp[key] = row[key]
            flights.append(temp)
            
        return flights # only one flight show up if there is one


def get_fare_conditions(ticket_no):
     with sql.connect("travel.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        query=f""" SELECT fare_conditions FROM ticket_flights where ticket_no = '{ticket_no}' """

        cursor.execute(query)
        data = cursor.fetchall()
        flights = []

        for row in data:
            temp = {}
            keys = row.keys()
            for key in keys:
                temp[key] = row[key]
            flights.append(temp)
            
        return flights # only one flight show up if there is one
     

def change_fare_condition(ticket_no):
    with sql.connect("travel.db") as con:
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("SELECT fare_conditions FROM ticket_flights WHERE ticket_no = ?", (ticket_no,))
        current_condition = cursor.fetchone()

        new_condition = "Economy" if current_condition[0] == "Business" else "Economy"

        # Update the fare_conditions in the database
        cursor.execute("UPDATE ticket_flights SET fare_conditions = ? WHERE ticket_no = ?", (new_condition, ticket_no))
        con.commit()