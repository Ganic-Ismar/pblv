from fastapi import APIRouter, HTTPException
from typing import List
from ..models.Car import Car, add_car, delete_car, read_cars

router = APIRouter()

@router.get("/cars", response_model=List[Car])
async def get_cars():
    try:
        return read_cars()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while reading the cars: "+str(e))

@router.post("/car")
async def create_car(car: Car):
    try:
        return add_car(car)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while adding the car: "+str(e))

@router.delete("/car/{car_id}")
async def remove_car(car_id: str):
    try:
        return delete_car(car_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while deleting the car: "+str(e))