import pandas as pd
import logging as logging
from pydantic import BaseModel
import os
from ..services.database_connector import get_database_connection
from datetime import date as Date
from datetime import time as Time
from datetime import datetime as DateTime
from typing import Optional

class ChargingplanItem(BaseModel):
    datetime: Optional[DateTime] = None
    pvPower: Optional[float] = None
    gridPower: Optional[float] = None


def chargingplanItemAddValues(item: ChargingplanItem, datetime: Date, pvPower: float, gridPower: float):
    item.datetime = datetime
    item.pvPower = pvPower
    item.gridPower = gridPower
    return item