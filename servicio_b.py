from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncio
import random
from datetime import datetime

app = FastAPI(title="Servicio B - Sensores Emulados")

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
        # Temperatura: entre 15 y 40 °C
        sensors_data["temperatura"]["value"] = round(random.uniform(15, 40), 2)

        # Humedad: entre 20 y 100 %
        sensors_data["humedad"]["value"] = round(random.uniform(20, 100), 2)

        # Lluvia: entre 0 y 20 mm (simulación de lluvia ligera o fuerte)
        sensors_data["lluvia"]["value"] = round(random.uniform(0, 20), 2)

        # Radiación solar: entre 0 y 1200 W/m²
        sensors_data["radiacion_solar"]["value"] = round(random.uniform(0, 1200), 2)

        # Timestamp de última actualización
        now = datetime.utcnow().isoformat()
        for sensor in sensors_data.values():
            sensor["last_update"] = now

        await asyncio.sleep(random.randint(1, 5))  # cambia dinámicamente cada 1–5 segundos

# Endpoint: obtener todos los sensores
@app.get("/all")
async def get_sensors():
    return JSONResponse(content=sensors_data)

# Endpoint: obtener un sensor específico
@app.get("/{sensor_id}")
async def get_sensor(sensor_id: str):
    if sensor_id not in sensors_data:
        return JSONResponse(content={"error": "Sensor no encontrado"}, status_code=404)
    return JSONResponse(content=sensors_data[sensor_id])

# Inicia la tarea de actualización en segundo plano
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_sensors())
