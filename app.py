import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



# 1.Correctly generate the engine to the correct sqlite file (2 points)

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# 2.Use automap_base() and reflect the database schema

Base = automap_base()
Base.prepare(engine)

# 3.Correctly save references to the tables in the sqlite file (measurement and station)

Measurement = Base.classes.measurement
Station = Base.classes.station

# 4.Correctly create and binds the session between the python app and database 

session = Session(bind=engine)

# 5.Display the available routes on the landing page
app = Flask(__name__)

# API Static Routes
@app.route("/")
def home():
     return (
        f"Welcome to the Hawaii Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"<br>"
    )
# A precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_data = session.query(Measurement.date, Measurement.prcp).all()

    prcp_dict = {} 
    for date, prcp in prcp_data:
        prcp_dict[date] = prcp
    return jsonify(prcp_dict)

# A stations route 
@app.route("/api/v1.0/stations")
def station():
    result = session.query(Station.station).all()
    station_list = list(np.ravel(result))
    return jsonify(station_list)

# A tobs route
@app.route("/api/v1.0/tobs")

def tobs():
    tobs = session.query(Measurement.tobs).\
            filter(Measurement.station == 'USC00519281' ).\
            filter(Measurement.date >= '2017,8,23').all()
    tobs_list = list(np.ravel(tobs))
    return jsonify(tobs_list)

# API Dynamic Route 
@app.route("/<start>")
@app.route("/<start>/<end>")
def start(start=None, end=None):
    if not end:
        start=dt.datetime.strptime(start,"%m-%d-%Y")
        result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
        return jsonify(list(np.ravel(result)))
    end = dt.datetime.strptime(end,"%m-%d-%Y")
    start=dt.datetime.strptime(start,"%m-%d-%Y")
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(list(np.ravel(result)))


if __name__ == "__main__":
    app.run(debug=True)