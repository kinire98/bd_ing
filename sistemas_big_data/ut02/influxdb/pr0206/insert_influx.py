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

SNo = "SNo"
name = "Name"
symbol = "Symbol"
date = "Date"
high = "High"
log = "Low"
open_ = "Open"
close_ = "Close"
volume = "Volume"
marketcap = "Marketcap"

def insert_influx(data: list[tuple[int, str, str, datetime, float, float, float, float, float, float]]):
    client = InfluxDBClient(
                url=INFLUX_URL,
                token=INFLUX_TOKEN,
                org="docs"
            )
    _insert_date()
    pass



def _insert_date(data: dict[str, Any], write_api: WriteApi) -> bool:
    print(data)
    print(write_api)
    return True

