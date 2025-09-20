import requests

BASE_URL = "https://mi-api.onrender.com/api/sensors"

# Todos los sensores
response = requests.get(f"{BASE_URL}/all")
print(response.json())

# Sensor específico
sensor = "temperatura"
response2 = requests.get(f"{BASE_URL}/{sensor}")
print(response2.json())