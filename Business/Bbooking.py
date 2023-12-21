import sqlite3 as sql
import random
import string


def generate_random_string(size=13, chars=string.digits):
    """Generates a random string with the given size and chars."""
    return "".join(random.choice(chars) for _ in range(size))


def generate_ticket_number():
    """Generates a random 13-digit ticket number."""
    return generate_random_string(size=13, chars=string.digits)


def generate_booking_reference():
    """Generates a random 6-character booking reference."""
    return generate_random_string(size=6, chars=string.ascii_uppercase + string.digits)


def buy_ticket(flight_id, name, id_number, fare_conditions, amount):
    with sql.connect("travel.db") as con:
        cursor = con.cursor()

        # Generate unique ticket_no and book_ref
        ticket_no = generate_ticket_number()
        book_ref = generate_booking_reference()

        # Ensure ticket_no and book_ref are unique
        while True:
            cursor.execute("SELECT * FROM tickets WHERE ticket_no = ?", (ticket_no,))
            if cursor.fetchone() is None:  # If there's no such ticket number
                break  # The ticket number is unique, exit the loop
            ticket_no = generate_ticket_number()  # Generate a new one and repeat

        while True:
            cursor.execute("SELECT * FROM tickets WHERE book_ref = ?", (book_ref,))
            if cursor.fetchone() is None:  # If there's no such booking reference
                break  # The booking reference is unique, exit the loop
            book_ref = generate_booking_reference()  # Generate a new one and repeat

        # Create a new ticket entry
        ticket_query = """
        INSERT INTO tickets (ticket_no, book_ref, passenger_id)
        VALUES (?, ?, ?)
        """
        cursor.execute(ticket_query, (ticket_no, book_ref, id_number))

        # Create a corresponding ticket_flights entry
        ticket_flights_query = """
        INSERT INTO ticket_flights (ticket_no, flight_id, fare_conditions, amount)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(
            ticket_flights_query, (ticket_no, flight_id, fare_conditions, amount)
        )

        # Commit the transaction
        con.commit()

    return ticket_no, id_number
