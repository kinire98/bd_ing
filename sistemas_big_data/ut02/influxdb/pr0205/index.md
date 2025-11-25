# PR0205
```python
from influxdb_client.client.write_api import ASYNCHRONOUS
from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write.point import Point
from influxdb_client.client.write_api import WriteOptions
from urllib3.exceptions import NewConnectionError
import psutil
import socket

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "MyInitialAdminToken0=="

def metricas_sistema():
    cpu_usage = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    ram_used_gb = round(mem.used / (1024**3) / 2)
    ram_percent = mem.percent

    disk = psutil.disk_usage("/")
    disk_usage = disk.percent

    return {
            "host": socket.gethostname(),
            "cpu_percent": cpu_usage,
            "ram_used_gb": ram_used_gb,
            "ram_percent": ram_percent,
            "disk_percent": disk_usage,
            }
def insert(pc_data, write_api):
        p = Point("medicion_pc")\
            .tag("metrics", "pc")\
            .field("host", pc_data["host"])\
            .field("cpu_percent", pc_data["cpu_percent"])\
            .field("ram_used_gb", pc_data["ram_used_gb"])\
            .field("ram_percent", pc_data["ram_percent"])\
            .field("disk_percent", pc_data["disk_percent"])\
            .time(None)
        write_api.write(bucket="test_bucket", org="docs", record=p)
print("--Iniciando conexion--")

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
        options = WriteOptions(
            batch_size=500,
            flush_interval=1000,
            write_type=ASYNCHRONOUS
            )
        write_api = client.write_api(write_options=options)
        while True:
            insert(metricas_sistema(), write_api)
    else:
        print("Error")
        print(f"    Error: {client.health().status}")
except (InfluxDBError, NewConnectionError) as e:
    print("[ERROR] Error al conectar con INfluxDB: ")
    print(f"    Detalle: {e}")
except  KeyboardInterrupt as key:
    print("Operacion finalizada por usuario")
finally:
    if client: # pyright: ignore
        client.close()
        print("--Conexion cerrada--")

```
