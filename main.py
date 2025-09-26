from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import random
from datetime import datetime
from collections import deque

app = FastAPI(title="API Principal con Sensores Emulados")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Guardar hasta 10,000 registros por sensor
MAX_RECORDS = 10000

sensors_data = {
    "temperatura": deque(maxlen=MAX_RECORDS),
    "humedad": deque(maxlen=MAX_RECORDS),
    "lluvia": deque(maxlen=MAX_RECORDS),
    "radiacion_solar": deque(maxlen=MAX_RECORDS),
}

# Coordenadas base (Villahermosa, Tabasco)
BASE_LAT = 17.9869
BASE_LON = -92.9303

def generate_fake_coordinates():
    """Genera coordenadas cercanas a la base"""
    lat = BASE_LAT + random.uniform(-0.05, 0.05)
    lon = BASE_LON + random.uniform(-0.05, 0.05)
    return {"lat": round(lat, 6), "lon": round(lon, 6)}

def generate_sensor_records():
    """Genera 10,000 registros iniciales de cada sensor"""
    now = datetime.utcnow().isoformat()
    for i in range(MAX_RECORDS):
        sensors_data["temperatura"].append({
            "value": round(random.uniform(15, 40), 2),
            "unit": "°C",
            "timestamp": now,
            "coords": generate_fake_coordinates()
        })
        sensors_data["humedad"].append({
            "value": round(random.uniform(20, 100), 2),
            "unit": "%",
            "timestamp": now,
            "coords": generate_fake_coordinates()
        })
        sensors_data["lluvia"].append({
            "value": round(random.uniform(0, 20), 2),
            "unit": "mm",
            "timestamp": now,
            "coords": generate_fake_coordinates()
        })
        sensors_data["radiacion_solar"].append({
            "value": round(random.uniform(0, 1200), 2),
            "unit": "W/m²",
            "timestamp": now,
            "coords": generate_fake_coordinates()
        })

# Inicia con 10,000 registros precargados
@app.on_event("startup")
async def startup_event():
    generate_sensor_records()

# Endpoints de sensores
@app.get("/api/sensors/all")
async def get_sensors():
    """Devuelve todos los registros de todos los sensores"""
    return JSONResponse(content={k: list(v) for k, v in sensors_data.items()})

@app.get("/api/sensors/{sensor_id}")
async def get_sensor(sensor_id: str):
    """Devuelve todos los registros de un sensor"""
    if sensor_id not in sensors_data:
        return JSONResponse(content={"error": "Sensor no encontrado"}, status_code=404)
    return JSONResponse(content=list(sensors_data[sensor_id]))

@app.get("/api/sensors/{sensor_id}/latest")
async def get_latest(sensor_id: str):
    """Devuelve el último valor de un sensor"""
    if sensor_id not in sensors_data:
        return JSONResponse(content={"error": "Sensor no encontrado"}, status_code=404)
    if not sensors_data[sensor_id]:
        return JSONResponse(content={"error": "No hay datos aún"}, status_code=404)
    return JSONResponse(content=sensors_data[sensor_id][-1])

# Endpoints de salud y raíz
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "API principal corriendo con 10,000 registros emulados con coordenadas"}
