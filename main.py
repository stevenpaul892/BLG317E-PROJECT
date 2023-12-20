# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import sqlite3 as sql

from flask import Flask, render_template, request, redirect
import sys

sys.path.append("../")
from Business import Baircrafts_data, Bairports_data, Bboarding_passes, Bbooking, Bflights, Bseats, Bticket_flights, Btickets


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
    print(cities)
    return render_template(
        "search_flight.html", optionsFrom=cities, optionsWhere=cities, optionsDates=[]
    )


@app.route("/searched_flights", methods=["POST"])
def searched_flights():
    selected_From = request.form["dropdownFrom"]
    selected_Where = request.form["dropdownWhere"]

    searched_flights = Bflights.search_flights(selected_From, selected_Where, 10)

    return render_template("searched_flights.html", flights=searched_flights)


@app.route("/buy_ticket", methods=["POST"])
def buy_ticket():
    selected_flight_id = request.form["flight_id"]
    return render_template("buy_ticket.html", flight_id=selected_flight_id)


@app.route("/show_ticket", methods=["POST"])
def show_ticket():
    return render_template("show_ticket.html")


@app.route("/show_ticket_error", methods=["GET"])
def show_ticket_error():
    return render_template("show_ticket_error.html")


##############################################################################################


@app.route("/check_in")
def check_in():
    return render_template("check_in.html")


@app.route("/boarding_pass")
def boarding_pass():
    selected_seats = Bseats.Search()
    return render_template("boarding_pass.html", seats=selected_seats)


@app.route("/show_boarding_pass")
def show_boarding_pass():
    return render_template("show_boarding_pass.html")


@app.route("/show_boarding_pass_error")
def show_boarding_pass_error():
    return render_template("show_boarding_pass_error.html")


###############################################################################################


@app.route("/check_flight_status")
def check_flight_status():
    return render_template("check_flight_status.html")

@app.route("/flight_status", methods=['POST'])
def flight_status():
    ticket_no = request.form["ticket_no"]

    selected_aircraft = Baircrafts_data.flight_status_search(ticket_no)
    print(ticket_no)
    print(selected_aircraft)
    return render_template("flight_status.html", aircraft=selected_aircraft)


@app.route("/flight_cancel")
def flight_cancel():
    return render_template("flight_cancel.html")


@app.route("/flight_cancel_error")
def flight_cancel_error():
    return render_template("flight_cancel_error.html")


# main driver function
if __name__ == "__main__":
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
