# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import sqlite3 as sql

from flask import Flask, render_template, request, redirect
import sys

import random

sys.path.append("../")
from Business import (
    Baircrafts_data,
    Bairports_data,
    Bboarding_passes,
    Bbooking,
    Bflights,
    Bseats,
    Bticket_flights,
    Btickets,
)


# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.


@app.route("/")  # redirects user to search flights page as default page
def index():
    return redirect("/search_flight")


@app.route("/search_flight")
def search_flight():
    cities = Bairports_data.get_cities()
    dates = Bflights.get_dates()
    return render_template(
        "search_flight.html",
        optionsFrom=cities,
        optionsWhere=cities,
        optionsDates=dates,
    )


@app.route("/searched_flights", methods=["POST"])
def searched_flights():
    selected_From = request.form["dropdownFrom"]
    selected_Where = request.form["dropdownWhere"]
    selected_When = request.form["dropdownWhen"]

    searched_flights = Bflights.search_flights(
        selected_From, selected_Where, selected_When
    )

    return render_template("searched_flights.html", flights=searched_flights)


@app.route("/buy_ticket", methods=["POST"])
def buy_ticket():
    selected_flight_id = request.form["flight_id"]

    return render_template("buy_ticket.html", flight_id=selected_flight_id)


@app.route("/show_ticket", methods=["POST"])
def show_ticket():
    flight_id = request.form["flight_id"]
    name = request.form["name_surname"]
    id = request.form["ID_number"]
    ticketNo, id_num = Bbooking.buy_ticket(flight_id, name, id, "ECO", 1)
    print(flight_id)

    return render_template(
        "show_ticket.html", flight_id=flight_id, ticketNo=ticketNo, id_num=id_num
    )


@app.route("/show_ticket_error", methods=["GET"])
def show_ticket_error():
    return render_template("show_ticket_error.html")


##############################################################################################


@app.route("/check_in")
def check_in():
    return render_template("check_in.html")


@app.route("/boarding_pass", methods=["POST"])
def boarding_pass():
    ticket_no = request.form["ticket_no"]
    ID = request.form["passenger_id"]

    if Btickets.check_ticket_existence(ticket_no, ID):
        if Bboarding_passes.boarding_pass_checkin(ticket_no):
            return redirect("/show_boarding_pass_error")

        seat = Bseats.get_empty_seat(ticket_no)
        flight_id = Bticket_flights.get_flight_from_ticket(ticket_no)[0]["flight_id"]
        flight = Bflights.get_flight_info_from_flight_id(flight_id)

        if Bboarding_passes.insert_boardinpass(
            ticket_no, flight_id, random.randint(1, 8), seat
        ):
            return render_template("boarding_pass.html", flight=flight, seat=seat)
        else:
            redirect("/show_boarding_pass_error")
    else:
        return redirect("/show_boarding_pass_error")


@app.route("/show_boarding_pass", methods=["POST"])
def show_boarding_pass():
    ticketNo = request.form["ticket_no"]
    flightNo = request.form["flight_no"]
    boardinPass = Bboarding_passes.boarding_pass_checkin(ticketNo, flightNo)

    return render_template("show_boarding_pass.html", passInfo=boardinPass)


@app.route("/show_boarding_pass_error")
def show_boarding_pass_error():
    return render_template("show_boarding_pass_error.html")


###############################################################################################


@app.route("/check_flight_status")
def check_flight_status():
    return render_template("check_flight_status.html")


@app.route("/flight_status", methods=["POST"])
def flight_status():
    ticket_no = request.form["ticket_no"]
    selected_aircraft = Baircrafts_data.flight_status_search(ticket_no)
    selected_flight = Bflights.flight_status_search(ticket_no)
    checkin_status = Bboarding_passes.check_checkin(ticket_no)

    return render_template(
        "flight_status.html",
        aircraft=selected_aircraft,
        flight=selected_flight,
        checkin=checkin_status,
    )


@app.route("/flight_cancel")
def flight_cancel():
    return render_template("flight_cancel.html")



@app.route("/check_ticket_number")
def check_ticket_number():
    return render_template("check_ticket_number.html")

@app.route("/manage_tickets", methods=["POST"])
def manage_tickets():
    ticket_no = request.form["ticket_no"]
    if_checked_in = Bboarding_passes.boarding_pass_checkin(ticket_no)
    fare_condition = Bticket_flights.get_fare_conditions(ticket_no)[0]['fare_conditions']
    return render_template("manage_tickets.html", if_checked_in = if_checked_in, fare_condition = fare_condition)

@app.route("/flight_cancel_error")
def flight_cancel_error():
    return render_template("flight_cancel_error.html")


# main driver function
if __name__ == "__main__":
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
