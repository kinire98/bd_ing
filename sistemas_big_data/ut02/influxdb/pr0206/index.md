# PR0206

`pr0206.py`

```python
import os

from extract_data import extract_data
from insert_influx import insert_influx

if __name__ == "__main__":
    base_dir = "./datasets/"
    coin_data = []
    for dir in os.listdir(path=base_dir):
        coin_data.append(extract_data(base_dir + dir))
    insert_influx(coin_data)

```

`extract_data.py`

```python
from datetime import datetime, timezone
def extract_data(file_name: str) -> list[tuple[int, str, str, datetime, float, float, float, float, float, float]]:
    values = []
    with open(file_name) as file:
        content = file.read()
    content = content.split("\n")
    for i in range(1, len(content) - 1):
        row_content = content[i].split(",")
        dt = datetime.strptime(row_content[3], "%Y-%m-%d %H:%M:%S")
        dt_utc = dt.replace(tzinfo=timezone.utc)
        time_date = dt_utc.isoformat().replace('+00:00', "Z")
        values.append((int(row_content[0]), row_content[1], row_content[2], time_date, row_content[4], row_content[5], row_content[6], row_content[7], row_content[8], row_content[9]))

    return values
```

`insert_influx.py`

```python
from influxdb_client.client.write_api import ASYNCHRONOUS
from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write.point import Point
from influxdb_client.client.write_api import WriteOptions, WriteApi
from urllib3.exceptions import NewConnectionError
from datetime import datetime
from typing import Any


INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "MyInitialAdminToken0=="

SNo_key = "SNo"
name_key = "Name"
symbol_key = "Symbol"
date_key = "Date"
high_key = "High"
low_key = "Low"
open_key = "Open"
close_key = "Close"
volume_key = "Volume"
marketcap_key = "Marketcap"

def insert_influx(data: list[list[tuple[int, str, str, datetime, float, float, float, float, float, float]]]):

    try:
        client = InfluxDBClient(
            url=INFLUX_URL,
            token=INFLUX_TOKEN,
            org="docs"
        )

        options = WriteOptions(write_type=ASYNCHRONOUS) # pyright: ignore
        write_api = client.write_api(write_options=options)
        datos_insertados = 0
        datos_no_insertados = 0
        for coin_data in data:
            print("New coin")
            mapped_data = list(map(lambda x: {
                SNo_key: x[0],
                name_key: x[1],
                symbol_key: x[2],
                date_key: x[3],
                high_key: x[4],
                low_key: x[5],
                open_key: x[6],
                close_key: x[7],
                volume_key: x[8],
                marketcap_key: x[9]
            }, coin_data))
        
            for temp_value in mapped_data:
                if _insert_date(temp_value, write_api):
                    datos_insertados += 1
                else:
                    datos_no_insertados += 1
        print("Insertados: ", datos_insertados)
        print("No insertados: ", datos_no_insertados)
    except NewConnectionError as nce:
        print("Error conectando: ", nce)
    except KeyboardInterrupt:
        print("Finalizado por usuario")



def _insert_date(data: dict[str, Any], write_api: WriteApi) -> bool:
    try:
        p = Point("crypto_value")\
            .tag("coin", data[name_key])\
            .field(high_key, float(data[high_key]))\
            .field(low_key, float(data[low_key]))\
            .field(open_key, float(data[open_key]))\
            .field(close_key, float(data[close_key]))\
            .field(volume_key, float(data[volume_key]))\
            .field(marketcap_key, float(data[marketcap_key]))\
            .time(data[date_key])
        write_api.write(bucket="crypto", org="docs", record=p)

        return True
    except InfluxDBError:
        return False

```
