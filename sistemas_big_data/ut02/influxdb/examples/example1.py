from influxdb_client.client.write_api import ASYNCHRONOUS
from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write.point import Point
from urllib3.exceptions import NewConnectionError



INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "MyInitialAdminToken0=="

print("--Iniciando conexion--")

def point(client):
    write_api = client.write_api(write_options=ASYNCHRONOUS)
    for i in range(1, 5000):
        p = Point("temperatura_medicion")\
            .tag("temp", "oficina")\
            .field("temp", i * 1.0)\
            .field("humid", 100 / i)\
            .time(None)
        write_api.write(bucket="test_bucket", org="docs", record=p)

try:
    client = InfluxDBClient(
                url=INFLUX_URL,
                token=INFLUX_TOKEN,
                org="docs"
            )
    print(f"Verificando estado de salud de InfluxDB en {INFLUX_URL}")
    if client.health().status == "pass":
        print("[INFO] Exito")
        print(f"Version: {client.version}")
        point(client)
    else:
        print("Error")
        print(f"    Error: {client.health().status}")
except (InfluxDBError, NewConnectionError) as e:
    print("[ERROR] Error al conectar con INfluxDB: ")
    print(f"    Detalle: {e}")
finally:
    if client: # pyright: ignore
        client.close()
        print("--Conexion cerrada--")


