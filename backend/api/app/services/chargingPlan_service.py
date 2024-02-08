import pandas as pd
from ..models.Car import Car, add_car, delete_car, read_cars
from ..models.Schedule import Schedule, add_schedule, delete_schedule, read_schedules
from ..models.Forecast import Forecast, read_forecasts
from .chargingplan_classes.Prognose_class import Prognose
from .chargingplan_classes.Fahrzeug_class import Fahrzeug
from .chargingplan_classes.Planung_class import Planung
from ..models.Chargingplan import Chargingplan

def chargingPlan_service()->list[Chargingplan]:
    #Create Chargingplan List
    chargingPlans = []
    #Get all cars from database
    cars = read_cars()
    #Create a list of all Fahrzeug objects
    fahrzeuge = []
    for car in cars:
        fahrzeug = Fahrzeug(car.id, car.modell, car.antrieb, car.kapatizaet, car.verbrauch, car.ladeleistung)
        fahrzeuge.append(fahrzeug)

        #Get the Fahrplan for each car from the database
        schedules = read_schedules(car.id)
        for schedule in schedules:
            fahrzeug.fahrplan_hinzufügen(schedule.arrival_date, schedule.arrival_time, schedule.departure_date, schedule.departure_time, schedule.required_charge)
    
    #Create a Prognose object
    prognose = Prognose()
    #Get all forecasts from the database
    forecasts = read_forecasts()
    #Add each forecast to the Prognose object
    for forecast in forecasts:
        prognose.prognose_hinzufügen(forecast.day, forecast.timeStart, forecast.timeEnd, forecast.watt)
    #Create a Planung object
    planung = Planung()
    
    #Create a charging plan for each car
    for fahrzeug in fahrzeuge:
        #Append the charging plan to the chargingPlans list
        chargingPlans.append(planung.erstelle_planung(prognose, fahrzeug))
    
    #Return the planung object
    return chargingPlans