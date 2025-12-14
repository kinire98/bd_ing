from influxdb_client.client.influxdb_client import InfluxDBClient

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "MyInitialAdminToken0=="
ORG = "docs"

QUERY_BUCKET = "crypto"

COIN = "Bitcoin"
FIELD = "Close"
QUERY = f"""
    data = from(bucket: "{QUERY_BUCKET}")
        |>range(start:1970-01-01T00:00:00Z)
        |>filter(fn: (r) => r.coin == "{COIN}" and r._field == "{FIELD}") 

    data
        |>aggregateWindow(every:1w, fn: min)
        |>yield(name: "weekly_min")

    data
        |>aggregateWindow(every:1w, fn: max)
        |>yield(name: "weekly_max")
"""

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)

query = client.query_api()

result = query.query(QUERY)

for table in result:
    for i in range(len(table.records)):
        if result[0].records[i]["_value"] and result[1].records[i]["_value"]:
            print("Date: ", result[0].records[i]["_time"].date())
            print("\tMin => ", result[0].records[i]["_value"])
            print("\tMax => ", result[1].records[i]["_value"])
    break
