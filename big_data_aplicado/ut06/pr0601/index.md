# PR0601. Capa bronce en Amazon AWS

## Carga de variables de entorno
De esta manera, las variables de entorno del _.env_ se cargarán cómo si fuesen una variable de entorno del sistema operativo


```python
from dotenv import load_dotenv
load_dotenv()
```




    True



## Carga de datos de playas


```python
import requests
import os
def consult_aemet(provence_code: int):
    API_ENDPOINT = f"https://opendata.aemet.es/opendata/api/prediccion/provincia/hoy/{provence_code}"
    params = {"api_key": os.getenv("AEMET_KEY")}
    try:
        response = requests.get(API_ENDPOINT, params=params)
        response.raise_for_status()
        new_url = response.json()["datos"]
        return requests.get(new_url).text
    except Exception as e:
        print(e)
        return None
```


```python
import boto3
BUCKET_NAME = "ing-iessanandres-big-data-aplicado"
def load_into_s3(name: str, data):
    session = boto3.Session(
        aws_access_key_id=os.getenv("aws_access_key_id"),
        aws_secret_access_key=os.getenv("aws_secret_access_key"),
        aws_session_token=os.getenv("aws_session_token"),
        region_name='us-east-1'
    )
    s3 = session.client("s3")
    s3.put_object(Bucket=BUCKET_NAME, Key=name, Body=data)
```


```python
BEACHES_FILE_NAME = "bronce/catalogos/guia_playas/v1/playas.csv"
with open("./Playas_españolas.csv") as f:
    data = f.read()
    load_into_s3(BEACHES_FILE_NAME, data)
```


```python
import numpy as np
import pandas as pd
import json
import time
from datetime import datetime

WEATHER_FILE_NAME = "bronce/meteorologia/prediccion_playas/"
today = datetime.now()
TIME_SUFFIX = f"year={today.year}/month={today.month}/day={today.day}/"
WEATHER_COMPLETE_PREFIX = WEATHER_FILE_NAME + TIME_SUFFIX


df_playas = pd.read_csv("./Playas_españolas.csv")

df_playas["consulta"] = df_playas["Provincia"] + np.where(df_playas["Isla"].isna() | (df_playas["Isla"] == "") | (df_playas["Isla"] == " "), "", " (" + df_playas["Isla"] + ")")


with open("./provincias.json") as f:
    provence_codes = json.load(f)
consulted = set()
for provence in df_playas["consulta"].unique():
    if provence_codes[provence] in consulted:
        continue
    data = consult_aemet(provence_codes[provence])
    print("Wait for API")
    time.sleep(5)
    if data is not None:
        consulted.add(provence_codes[provence])
        load_into_s3(WEATHER_COMPLETE_PREFIX + provence + ".txt", data)
        print("Loaded file")
    else:
        print("Error")

```

    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    429 Client Error: Too Many Requests for url: https://opendata.aemet.es/opendata/api/prediccion/provincia/hoy/46?api_key=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJpa25pdGdhcnJpQGdtYWlsLmNvbSIsImp0aSI6ImE5ZjZjZWQ4LTNmZjctNDA2Yi05ZGU2LTA5NzgxZmU2MzRmNCIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNzc1NjQ5MjQyLCJ1c2VySWQiOiJhOWY2Y2VkOC0zZmY3LTQwNmItOWRlNi0wOTc4MWZlNjM0ZjQiLCJyb2xlIjoiIn0.3To847WZHWSLC39-n2CF8V0GB-JvDpAY0S1czy1S6go
    Wait for API
    Error
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file
    Wait for API
    Loaded file


## Pruebas de funcionamiento
### Archivo playas
![](./playas.png)
### Archivos de previsiones
![](./prevision.png)


