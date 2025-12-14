from influxdb_client.client.influxdb_client import InfluxDBClient

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "MyInitialAdminToken0=="
ORG = "docs"


QUERY_BUCKET = "crypto"

COIN = "Bitcoin"
FIELD = "Close"

QUERY = f"""
from(bucket: "{QUERY_BUCKET}")
    |> range(start: 2020-01-01T00:00:00Z, stop: 2020-12-31T23:59:59Z)
    |> filter(fn: (r) => r.coin == "{COIN}" and r._field == "{FIELD}")
"""
# 
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)

query = client.query_api()

result = query.query(org=ORG, query=QUERY)


for table in result:
    for record in table.records:
        print(record["_value"])

