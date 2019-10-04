from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

one_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

app = Flask(__name__)

@app.route("/")
def Home():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"     
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    results = session.query(Measurement.prcp, Measurement.date).all()
    session.close()
    
    precipitation = []
    for precip, date in results:
        precipitation_dict = {}
        precipitation_dict["precip"] = prcp
        precipitation_dict["date"] = date
        precipitation.append(precipitation_dict)
    
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    results = session.query(Measurement.station, Station.station, Station.name).\
        filter(Measurement.station == Station.station).all()
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def temp_obs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= one_year_date).all()
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start_date_only(start):
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date > start).all()
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start, end):
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date > start, Measurement.date < end).all()
    session.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)