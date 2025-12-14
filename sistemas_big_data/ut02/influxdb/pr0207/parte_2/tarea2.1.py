from influxdb_client.client.influxdb_client import InfluxDBClient

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "MyInitialAdminToken0=="
ORG = "docs"

QUERY_BUCKET = "crypto"

COIN = "Bitcoin"
FIELD = "Close"
QUERY = f"""
    from(bucket: "{QUERY_BUCKET}")
        |>range(start:1970-01-01T00:00:00Z)
        |>filter(fn: (r) => r.coin == "{COIN}" and r._field == "{FIELD}") 
        |>aggregateWindow(every:1mo, fn: mean)
"""

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)

query = client.query_api()

result = query.query(QUERY)

for table in result:
    for record in table.records:
        if record["_value"]:
            print("Month: ", record["_time"], " => ", record["_value"])
