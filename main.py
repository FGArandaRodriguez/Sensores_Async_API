from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from servicio_b import app as sensores_app  # importamos la app de servicio_b
from fastapi.routing import Mount

# App principal
app = FastAPI(title="API Principal con Sensores")

# Middleware CORS (para que tu app móvil pueda llamar la API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción pon la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montamos la app de servicio_b en un sub-path
app.mount("/api/sensors", sensores_app)

# Endpoint básico de salud
@app.get("/health")
def health():
    return {"status": "ok"}

# Endpoint raíz
@app.get("/")
def root():
    return {"message": "API principal corriendo con sensores emulados"}
