from fastapi import APIRouter, HTTPException
from typing import List
from ..services.chargingPlan_service import chargingPlan_service
from ..models.Chargingplan import Chargingplan

router = APIRouter()

@router.get("", response_model=List[Chargingplan])
async def get_chargingPlan():
    return chargingPlan_service()
