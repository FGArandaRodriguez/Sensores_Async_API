from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import random
from datetime import datetime

app = FastAPI(title="API Principal con Sensores Emulados")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sensores virtuales
sensors_data = {
    "temperatura": {"value": 0.0, "unit": "°C", "last_update": None},
    "humedad": {"value": 0.0, "unit": "%", "last_update": None},
    "lluvia": {"value": 0.0, "unit": "mm", "last_update": None},
    "radiacion_solar": {"value": 0.0, "unit": "W/m²", "last_update": None},
}

# Función que actualiza los sensores cada 1–5 segundos
async def update_sensors():
    while True:
        sensors_data["temperatura"]["value"] = round(random.uniform(15, 40), 2)
        sensors_data["humedad"]["value"] = round(random.uniform(20, 100), 2)
        sensors_data["lluvia"]["value"] = round(random.uniform(0, 20), 2)
        sensors_data["radiacion_solar"]["value"] = round(random.uniform(0, 1200), 2)
        now = datetime.utcnow().isoformat()
        for sensor in sensors_data.values():
            sensor["last_update"] = now
        await asyncio.sleep(random.randint(1, 5))

# Inicia la tarea de actualización en segundo plano
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_sensors())

# Endpoints de sensores
@app.get("/api/sensors/all")
async def get_sensors():
    return JSONResponse(content=sensors_data)

@app.get("/api/sensors/{sensor_id}")
async def get_sensor(sensor_id: str):
    if sensor_id not in sensors_data:
        return JSONResponse(content={"error": "Sensor no encontrado"}, status_code=404)
    return JSONResponse(content=sensors_data[sensor_id])

# Endpoints de salud y raíz
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "API principal corriendo con sensores emulados"}
