# PR0207: Consultas con Flux

## PARTE I: Consultas de filtrado y estructura

### Tarea 1.1: Precio de cierre de Bitcoin
```python
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

```
### Tarea 1.2: Volumen Total del Ethereum (ETHUSDT)
```python
from influxdb_client.client.influxdb_client import InfluxDBClient

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "MyInitialAdminToken0=="
ORG = "docs"

QUERY_BUCKET = "crypto"

COIN = "Ethereum"
FIELD = "Volume"
QUERY = f"""
    from(bucket: "{QUERY_BUCKET}")
        |>range(start: 2021-01-01T00:00:00Z, stop: 2021-06-30T23:59:59Z)
        |>filter(fn: (r) => r.coin == "{COIN}" and r._field == "{FIELD}") 
        |>sum()
"""

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)

query = client.query_api()

result = query.query(QUERY)

for table in result:
    for record in table.records:
        print(record["_value"])
```

## PARTE II: Agregación temporal 
### Tarea 2.1: Precio promedio mensual
```python
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
```
### Tarea 2.2: Rango de volatilidad
```python
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
```
## PARTE III: Manipulación y Joins
### Tarea 3.1: Cálculo de variación porcentual diaria (Map)
```python
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
        print("\tPercent changed: ", "{0:.2f}".format(record["difference"]) + "%")
```
### Tarea 3.2: Comparación de precios de cierre (Join)
```python
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
```
