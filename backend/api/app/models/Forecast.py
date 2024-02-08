import pandas as pd
import logging as logging
from pydantic import BaseModel
import os
from ..services.database_connector import get_database_connection
from datetime import date as Date
from datetime import time as Time
import logging

log = logging.getLogger(__name__)

class Forecast:
    day: Date
    timeStart: Time
    timeEnd: Time
    watt: float

    def __init__(self, day: Date, timeStart: Time, timeEnd: Time, watt: float):
        self.day = day
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.watt = watt

def read_forecasts():
    db_connection = get_database_connection()
    df = pd.read_sql_query("SELECT * FROM Prognose", db_connection)
    forecasts = []
    for _, row in df.iterrows():
        forecast = Forecast(day=row[0], timeStart=row[1], timeEnd=row[2], watt=row[3])
        forecasts.append(forecast)
    return forecasts
