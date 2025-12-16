
from influxdb_client.client.influxdb_client import InfluxDBClient


INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "MyInitialAdminToken0=="
ORG = "docs"

QUERY_BUCKET = "crypto"

FIELD = "Close"
LBRACKET = "{"
RBRACKET = "}"
QUERY = """
    import "join"
    data = from(bucket: "crypto")
        |>range(start:2020-01-01T00:00:00Z, stop: 2020-12-31T23:59:59Z)
        |>filter(fn: (r) => r._field == "Close")
        |>truncateTimeColumn(unit:1m)

    btc_data = data  
        |>filter(fn: (r) => r.coin == "Bitcoin") 
        |>drop(columns: ["coin"])

    eth_data = data
        |>filter(fn: (r) => r.coin == "Ethereum") 
        |>drop(columns: ["coin"])


        join.inner(
        left: btc_data,
        right: eth_data,
        on: (l, r) => l._time == r._time,
        as: (l, r) => ({l with diff: l._value / r._value})
        )
"""

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)


query_api = client.query_api()


result = query_api.query(QUERY)

for table in result:
    for record in table.records:
        print("Date: ", record["_time"].date())
        print("\t", "{0:.2f}".format(record["diff"]) + "%")
