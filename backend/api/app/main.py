from fastapi import FastAPI
from .routers.car_router import router as car_router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(car_router, prefix="/cars", tags=["cars"])