import pandas as pd
import logging as logging
from pydantic import BaseModel
import os
from ..services.database_connector import get_database_connection
from datetime import date as Date
from datetime import time as Time

# Define logger
log = logging.getLogger(__name__)

class Schedule(BaseModel):
    id: int | None = None
    car_id: int
    arrival_date: Date
    arrival_time: Time
    departure_date: Date
    departure_time: Time
    required_charge: float

def add_schedule(schedule: Schedule):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        
        #Get highest id from database
        cursor.execute("SELECT MAX(id) FROM Fahrten")
        max_id = cursor.fetchone()
        if max_id[0] == None:
            max_id = 0
        else:
            max_id = max_id[0]
        max_id += 1

        # Format dates as strings
        arrival_date_str = schedule.arrival_date.strftime("%Y-%m-%d")
        arrival_time_str = schedule.arrival_time.strftime("%H:%M:%S")
        departure_date_str = schedule.departure_date.strftime("%Y-%m-%d")
        departure_time_str = schedule.departure_time.strftime("%H:%M:%S")

        #Insert new schedule into database
        cursor.execute("INSERT INTO Fahrten (id, fahrzeug, ankunftTag, ankunftUhrzeit, abfahrtTag, abfahrtUhrzeit, notwendigeLadung) VALUES ("+str(max_id)+","+str(schedule.car_id)+",'"+arrival_date_str+"','"+ arrival_time_str +"','"+ departure_date_str +"','"+ departure_time_str+"',"+ str(schedule.required_charge) + ")")
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        logging.error("Error while adding schedule to database: " + str(e))
        return False

def delete_schedule(schedule_id: int):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Fahrten WHERE id = " + str(schedule_id))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        logging.error("Error while deleting schedule from database: " + str(e))
        return False

def read_all_schedules():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Fahrten")
        schedules = cursor.fetchall()
        connection.close()
        # Parse the results into a list of Schedule objects
        schedules = [Schedule(id=row[0], car_id=row[1], arrival_date=row[2], arrival_time=row[3], departure_date=row[4], departure_time=row[5], required_charge=row[6]) for row in schedules]
        return schedules
    except Exception as e:
        logging.error("Error while reading schedules from database: " + str(e))
        return False
def read_schedules(car_id:int)->list:
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Fahrten WHERE fahrzeug =" + str(car_id))
        schedules = cursor.fetchall()
        connection.close()
        # Parse the results into a list of Schedule objects
        schedules = [Schedule(id=row[0], car_id=row[1], arrival_date=row[2], arrival_time=row[3], departure_date=row[4], departure_time=row[5], required_charge=row[6]) for row in schedules]
        return schedules
    except Exception as e:
        logging.error("Error while reading schedules from database: " + str(e))
        return False
