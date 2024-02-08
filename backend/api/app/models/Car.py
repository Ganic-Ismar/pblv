import pandas as pd
import logging as logging
from pydantic import BaseModel
import os
from ..services.database_connector import get_database_connection

log = logging.getLogger(__name__)


class Car(BaseModel):
    id: int | None = None
    modell: str
    antrieb: str
    kapatizaet: int
    verbrauch: float
    ladeleistung: float


def read_cars()->list[Car]:
    try:
        print(os.environ.get('POSTGRES_HOST'))
        db_connection = get_database_connection()
        df = pd.read_sql_query("SELECT * FROM Fahrzeuge", db_connection)
        cars = []
        for _, row in df.iterrows():
            car = Car(id=row['id'], modell=row['modell'], antrieb=row['antrieb'], kapatizaet=row['kapatizaet'], verbrauch=row['verbrauch'], ladeleistung=row['ladeleistung'])
            cars.append(car)
        return cars
    except Exception as e:
        log.error('Error while reading cars')
        raise e

def add_car(car: Car):
    try:
        db_connection = get_database_connection()
        cursor = db_connection.cursor()
        # Get highst id
        cursor.execute("SELECT MAX(id) FROM Fahrzeuge")
        max_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO Fahrzeuge (id, modell, antrieb, kapatizaet, verbrauch, ladeleistung) VALUES ("+str(max_id+1)+", '"+car.modell+"','"+car.antrieb+"',"+str(car.kapatizaet)+","+str(car.verbrauch)+","+str(car.ladeleistung)+")")
        db_connection.commit()
        car.id = max_id+1

    except Exception as e:
        log.error('Error while adding car')
        raise e
    return car

def delete_car(key: int):
    try:
        db_connection = get_database_connection()
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM Fahrzeuge WHERE id="+str(key))
    except Exception as e:
        log.error('Error while deleting car:')
        raise e
    return True