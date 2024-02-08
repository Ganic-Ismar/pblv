from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.car_router import router as car_router
from .routers.chargingplan_router import router as chargingplan_router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Add CORS Policy
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:800",
    "http://localhost:8000",
    "http://localhost:80"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(car_router, prefix="/cars", tags=["cars"])

app.include_router(chargingplan_router, prefix="/chargingplan", tags=["chargingplan"])