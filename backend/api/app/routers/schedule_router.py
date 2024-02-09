from fastapi import APIRouter, HTTPException
from typing import List
from ..models.Schedule import Schedule, add_schedule, delete_schedule, read_schedules, read_all_schedules

router = APIRouter()

@router.get('/{id}', response_model=List[Schedule])
async def get_schedule(id: int):
    try:
        return read_schedules(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while reading the schedules: "+str(e))

@router.get('', response_model=List[Schedule])
async def get_schedules():
    try:
        return read_all_schedules()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while reading the schedules: "+str(e))
    
@router.post('')
async def create_schedule(schedule: Schedule):
    try:
        return add_schedule(schedule)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while adding the schedule: "+str(e))

@router.delete('/{id}')
async def remove_schedule(id: int):
    try:
        return delete_schedule(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while deleting the schedule: "+str(e))