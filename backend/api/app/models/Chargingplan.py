from pydantic import BaseModel
from .ChargingplanItem import ChargingplanItem
from typing import List, Optional

class Chargingplan(BaseModel):
    carId: Optional[int] = None
    items: Optional[List[ChargingplanItem]] = []

    class Config:
        validate_assignment = True

    
def add_item(chargingplan:Chargingplan, item: ChargingplanItem):
        chargingplan.items.append(item)
    
def setCarId(chargingplan:Chargingplan, carId: int):
    chargingplan.carId = carId