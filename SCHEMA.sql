CREATE DATABASE Airlines;
USE Airlines;

-- Table: aircrafts_data
CREATE TABLE aircrafts_data (
    aircraft_code CHARACTER(3) PRIMARY KEY,
    model JSON NOT NULL,
    ramge INTEGER NOT NULL
);

-- Table: airports_data
CREATE TABLE airports_data (
    airport_code CHARACTER(3) PRIMARY KEY,
    airport_name JSON NOT NULL,
    city JSON NOT NULL,
    coordinates POINT NOT NULL,
    timezone TEXT NOT NULL
);

-- Table: bookings
CREATE TABLE bookings (
    book_ref CHARACTER(6) PRIMARY KEY,
    book_date TIMESTAMP  NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL
);

-- Table: tickets
CREATE TABLE tickets (
    ticket_no CHARACTER(13) PRIMARY KEY,
    book_ref CHARACTER(6) NOT NULL,
    passenger_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (book_ref) REFERENCES bookings (book_ref)
);

-- Table: flights
CREATE TABLE flights (
    flight_id SERIAL PRIMARY KEY,
    flight_no CHARACTER(6) NOT NULL,
    scheduled_departure TIMESTAMP  NOT NULL,
    scheduled_arrival TIMESTAMP  NOT NULL,
    departure_airport CHARACTER(3) NOT NULL,
    arrival_airport CHARACTER(3) NOT NULL,
    status VARCHAR(20) NOT NULL,
    aircraft_code CHARACTER(3) NOT NULL,
    actual_departure TIMESTAMP,
    actual_arrival TIMESTAMP,
    FOREIGN KEY (departure_airport) REFERENCES airports_data (airport_code),
    FOREIGN KEY (arrival_airport) REFERENCES airports_data (airport_code),
    FOREIGN KEY (aircraft_code) REFERENCES aircrafts_data (aircraft_code)
);

-- Table: seats
CREATE TABLE seats (
    aircraft_code CHAR(3),
    seat_no VARCHAR(4),
    fare_conditions VARCHAR(10),
    PRIMARY KEY (aircraft_code, seat_no), -- Add a primary key constraint
    INDEX seat_index (seat_no) -- Add an index on the seat_no column
);

-- Table: boarding_passes
CREATE TABLE boarding_passes (
    ticket_no CHARACTER(13) PRIMARY KEY,
    flight_id SERIAL NOT NULL,
    boarding_no INTEGER NOT NULL,
    seat_no VARCHAR(4) NOT NULL,
    FOREIGN KEY (ticket_no) REFERENCES tickets (ticket_no),
    FOREIGN KEY (flight_id) REFERENCES flights (flight_id),
    FOREIGN KEY (seat_no) REFERENCES seats (seat_no)
);

-- Table: ticket_flights
CREATE TABLE ticket_flights (
    ticket_no CHARACTER(13) NOT NULL,
    flight_id SERIAL NOT NULL,
    fare_conditions VARCHAR(10) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (ticket_no, flight_id),
    FOREIGN KEY (ticket_no) REFERENCES tickets (ticket_no),
    FOREIGN KEY (flight_id) REFERENCES flights (flight_id)
);

