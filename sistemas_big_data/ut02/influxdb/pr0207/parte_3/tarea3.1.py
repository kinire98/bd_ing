import re
from influxdb_client.client.influxdb_client import InfluxDBClient


INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "MyInitialAdminToken0=="
ORG = "docs"

QUERY_BUCKET = "crypto"

COIN_1 = "Tether"
COIN_2 = "USD Coin"
FIELD = "Close"
LBRACKET = "{"
RBRACKET = "}"
QUERY = """
    from(bucket: "crypto")
        |>range(start:2016-01-01T00:00:00Z, stop: 2018-12-31T23:59:59Z)
        |>filter(fn: (r) => (r.coin == "Tether" or r.coin == "USD Coin") and r._field == "Close") 
        |>duplicate(column: "_value", as: "_cur_value")
        |>difference()
        |> map(fn: (r) => ({ r with difference: (r._value / (r._cur_value - r._value)) * 100.0}))
"""

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)


query_api = client.query_api()


result = query_api.query(QUERY)

for table in result:
    for record in table.records:
        print("Day: ", record["_time"].date())
        print("\tPercent changed: ", str(record["difference"]) + "%")
