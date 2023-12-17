# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import sqlite3 as sql

from flask import Flask, render_template, request
import sys

sys.path.append("../")
from Business import Baircrafts_data


# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.


@app.route("/")
def index():
    args = request.args
    aircrafts = Baircrafts_data.Search()

    return render_template("index.html", data=aircrafts)


@app.route("/flight")
def flight():
    args = request.args
    aircrafts = Baircrafts_data.Search()

    return render_template("flight.html", data=aircrafts)


# main driver function
if __name__ == "__main__":
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
