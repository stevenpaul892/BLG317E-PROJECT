# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import sqlite3 as sql

from flask import Flask, render_template, request, redirect, url_for
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
app.static_folder = 'static'

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
    selected_When = request.form["departureDate"]

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
            return redirect(url_for("error_page",
                                     error_message="You are already checked in.",
                                     recommendation="You can see your seat number in flight status page."))

        seat = Bseats.get_empty_seat(ticket_no)
        flight_id = Bticket_flights.get_flight_from_ticket(ticket_no)[0]["flight_id"]
        flight = Bflights.get_flight_info_from_flight_id(flight_id)

        if Bboarding_passes.insert_boardinpass(
            ticket_no, flight_id, random.randint(1, 8), seat
        ):
            return render_template("boarding_pass.html", flight=flight, seat=seat)
        else:
            return redirect(url_for("error_page",
                                     error_message="Sorry, there was an error.",
                                     recommendation="Please try to check in again."))
    else:
        return redirect(url_for("error_page",
                                 error_message="Sorry, we couldn't find your ticket.",
                                 recommendation="Please check your ticket number and ID."))


@app.route("/show_boarding_pass", methods=["POST"])
def show_boarding_pass():
    ticketNo = request.form["ticket_no"]
    flightNo = request.form["flight_no"]
    boardinPass = Bboarding_passes.boarding_pass_checkin(ticketNo, flightNo)

    return render_template("show_boarding_pass.html", passInfo=boardinPass)


@app.route("/error_page/<error_message>/<recommendation>")
def error_page(error_message, recommendation):
    return render_template("error_page.html", error_message=error_message, recommendation=recommendation)


###############################################################################################


@app.route("/check_flight_status")
def check_flight_status():
    return render_template("check_flight_status.html")


@app.route("/flight_status", methods=["POST"])
def flight_status():
    ticket_no = request.form["ticket_no"]

    if Btickets.check_ticket_existence_without_ID(ticket_no):
        selected_aircraft = Baircrafts_data.flight_status_search(ticket_no)
        selected_flight = Bflights.flight_status_search(ticket_no)
        checkin_status = Bboarding_passes.check_checkin(ticket_no)

        return render_template(
            "flight_status.html",
            aircraft=selected_aircraft,
            flight=selected_flight,
            checkin=checkin_status,
        )
    else:
        return redirect(url_for("error_page",
                                 error_message="Sorry, we couldn't find your ticket.",
                                 recommendation="Please check your ticket number."))


@app.route("/check_ticket_number")
def check_ticket_number():
    return render_template("check_ticket_number.html")

@app.route("/manage_tickets", methods=["POST"])
def manage_tickets():
    ticket_no = request.form["ticket_no"]
    ID = request.form["passenger_id"]

    if Btickets.check_ticket_existence(ticket_no, ID):
        if_checked_in = Bboarding_passes.boarding_pass_checkin(ticket_no)
        fare_condition = Bticket_flights.get_fare_conditions(ticket_no)[0]['fare_conditions']
        return render_template("manage_tickets.html", if_checked_in = if_checked_in, fare_condition = fare_condition, h_ticket_no = ticket_no)
    else:
        return redirect(url_for("error_page",
                                 error_message="Sorry, we couldn't find your ticket.",
                                 recommendation="Please check your ticket number and ID."))
    
@app.route('/degrade_ticket', methods=['POST'])
def degrade_ticket():
    ticket_no = request.form["ticket_no"]
    if Bticket_flights.change_fare_condition(ticket_no):
        return render_template('message_page.html', message='Your ticket has been downgraded from Business to Economy.')
    else:
        return redirect(url_for("error_page",
                                 error_message="Sorry, there was an error while downgrading your ticket.",
                                 recommendation="Please try again."))

@app.route('/upgrade_ticket', methods=['POST'])
def upgrade_ticket():
    ticket_no = request.form["ticket_no"]
    if Bticket_flights.change_fare_condition(ticket_no):
        return render_template('message_page.html', message='Your ticket has been upgraded from Economy to Business.')
    else:
        return redirect(url_for("error_page",
                                 error_message="Sorry, there was an error while upgrading your ticket.",
                                 recommendation="Please try again."))

@app.route('/cancel_flight', methods=['POST'])
def cancel_flight():
    ticket_no = request.form["ticket_no"]
    if Btickets.cancel_ticket(ticket_no):
        return render_template('message_page.html', message='Your ticket is successfully cancelled.')
    else:
        return redirect(url_for("error_page",
                                 error_message="Sorry, there was an error while cancelling your ticket.",
                                 recommendation="Please try again."))
# main driver function
if __name__ == "__main__":
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
