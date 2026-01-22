# PR0501. Ingesta de datos de ficheros CSV

## Dataset 1: Datos para la predicción del rendimiento en cultivos


```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
schema = StructType([
    StructField("Crop", StringType(), False),
    StructField("Region", StringType(), False),
    StructField("Soil_Type", StringType(), False),
    StructField("Soil_pH", DoubleType(), False),
    StructField("Rainfall_mm", DoubleType(), False),
    StructField("Temperature_C", DoubleType(), False),
    StructField("Humidity_pct", DoubleType(), False),
    StructField("Fertilizar_Used_kg", DoubleType(), False),
    StructField("Irrigation", StringType(), False),
    StructField("Pesticides_Used_kg", DoubleType(), False),
    StructField("Planting_Density", DoubleType(), False),
    StructField("Previous_Crop", StringType(), False),
    StructField("Yield_ton_per_ha", DoubleType(), False),
])
schema.fields
```




    [StructField('Crop', StringType(), False),
     StructField('Region', StringType(), False),
     StructField('Soil_Type', StringType(), False),
     StructField('Soil_pH', DoubleType(), False),
     StructField('Rainfall_mm', DoubleType(), False),
     StructField('Temperature_C', DoubleType(), False),
     StructField('Humidity_pct', DoubleType(), False),
     StructField('Fertilizar_Used_kg', DoubleType(), False),
     StructField('Irrigation', StringType(), False),
     StructField('Pesticides_Used_kg', DoubleType(), False),
     StructField('Planting_Density', DoubleType(), False),
     StructField('Previous_Crop', StringType(), False),
     StructField('Yield_ton_per_ha', DoubleType(), False)]




```python
from pyspark.sql import SparkSession
spark = ( SparkSession.builder
            .appName("pruebas")
            .master("spark://spark-master:7077")
            .getOrCreate()
        )
df = (
    spark.read
        .format("csv")
        .schema(schema)
        .option("header", "true")
        .load("/workspace/pr0501/crop_yield_dataset.csv")
)
```

### 1.-Selección de características


```python
df_sel = df.select("Crop", "Region", "Temperature_C", "Rainfall_mm", "Irrigation", "Yield_ton_per_ha")
df_sel
```




    DataFrame[Crop: string, Region: string, Temperature_C: double, Rainfall_mm: double, Irrigation: string, Yield_ton_per_ha: double]



### 2.-Normalización de los nombres


```python
df_renamed = df_sel\
    .withColumnRenamed("Temperature_C", "Temperatura") \
    .withColumnRenamed("Rainfall_mm", "Lluvia") \
    .withColumnRenamed("Yield_ton_per_ha", "Rendimiento")
df_renamed
```




    DataFrame[Crop: string, Region: string, Temperatura: double, Lluvia: double, Irrigation: string, Rendimiento: double]



### 3.-Filtrado de datos (`filter`)


```python
from pyspark.sql.functions import col, lit
df_filtered = df_renamed.filter((col("Crop") == "Maize") & (col("Temperatura") > 25))
df_filtered.show(3)
```

                                                                                    

    +-----+--------+-----------+------+----------+-----------+
    | Crop|  Region|Temperatura|Lluvia|Irrigation|Rendimiento|
    +-----+--------+-----------+------+----------+-----------+
    |Maize|Region_D|       26.4|1054.3|      Drip|     169.06|
    |Maize|Region_C|       32.4| 846.1|      None|      162.2|
    |Maize|Region_A|       26.6| 362.5| Sprinkler|      95.23|
    +-----+--------+-----------+------+----------+-----------+
    only showing top 3 rows
    


### 4.-Encadenamiento


```python
df_all_in_one = df \
    .select("Crop", "Region", "Temperature_C", "Rainfall_mm", "Irrigation", "Yield_ton_per_ha") \
    .withColumnRenamed("Temperature_C", "Temperatura") \
    .withColumnRenamed("Rainfall_mm", "Lluvia") \
    .withColumnRenamed("Yield_ton_per_ha", "Rendimiento") \
    .filter((col("Crop") == "Maize") & (col("Temperatura") > 25))
df_all_in_one.show(5)

```

    +-----+--------+-----------+------+----------+-----------+
    | Crop|  Region|Temperatura|Lluvia|Irrigation|Rendimiento|
    +-----+--------+-----------+------+----------+-----------+
    |Maize|Region_D|       26.4|1054.3|      Drip|     169.06|
    |Maize|Region_C|       32.4| 846.1|      None|      162.2|
    |Maize|Region_A|       26.6| 362.5| Sprinkler|      95.23|
    |Maize|Region_C|       33.7|1193.3|      None|     110.57|
    |Maize|Region_C|       27.8| 695.2|     Flood|     143.84|
    +-----+--------+-----------+------+----------+-----------+
    only showing top 5 rows
    


## Dataset 2: Lugares famosos del mundo


```python
from pyspark.sql.types import IntegerType
schema = StructType([
    StructField("Place_Name", StringType(), False),
    StructField("Country", StringType(), False),
    StructField("City", StringType(), False),
    StructField("Annual_Visitors_Millions", IntegerType(), False),
    StructField("Type", StringType(), False),
    StructField("UNESCO_World_Heritage", StringType(), False),
    StructField("Year_Build", StringType(), False),
    StructField("Entry_Fee_USD", IntegerType(), False),
    StructField("Best_Visit_Month", StringType(), False),
    StructField("Region", StringType(), False),
    StructField("Tourism_Revenue_Million_USD", IntegerType(), False),
    StructField("Average_Visit_Duration_Hours", DoubleType(), False),
    StructField("Famous_For", StringType(), False),
])

schema.fields
```




    [StructField('Place_Name', StringType(), False),
     StructField('Country', StringType(), False),
     StructField('City', StringType(), False),
     StructField('Annual_Visitors_Millions', IntegerType(), False),
     StructField('Type', StringType(), False),
     StructField('UNESCO_World_Heritage', StringType(), False),
     StructField('Year_Build', StringType(), False),
     StructField('Entry_Fee_USD', IntegerType(), False),
     StructField('Best_Visit_Month', StringType(), False),
     StructField('Region', StringType(), False),
     StructField('Tourism_Revenue_Million_USD', IntegerType(), False),
     StructField('Average_Visit_Duration_Hours', DoubleType(), False),
     StructField('Famous_For', StringType(), False)]




```python
from pyspark.sql import SparkSession
spark = ( SparkSession.builder
            .appName("pruebas")
            .master("spark://spark-master:7077")
            .getOrCreate()
        )
df = (
    spark.read
        .format("csv")
        .schema(schema)
        .option("header", "true")
        .load("/workspace/pr0501/world_famous_places_2024.csv")
)
```

    Setting default log level to "WARN".
    To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
    26/01/22 08:42:48 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable


#### 1.-Selección de datos críticos


```python
df_base = df.select("Place_Name", "Country", "UNESCO_World_Heritage", "Entry_Fee_USD", "Annual_Visitors_Millions")
df_base
```




    DataFrame[Place_Name: string, Country: string, UNESCO_World_Heritage: string, Entry_Fee_USD: int, Annual_Visitors_Millions: int]



### 2.-Traducción y simplificación


```python
df_es = df_base \
    .withColumnRenamed("Place_Name", "Lugar") \
    .withColumnRenamed("UNESCO_World_Heritage", "Es_UNESCO") \
    .withColumnRenamed("Entry_Fee_USD", "Precio_Entrada") \
    .withColumnRenamed("Annual_Visitors_Millions", "Visitantes_Millones")
df_es
```




    DataFrame[Lugar: string, Country: string, Es_UNESCO: string, Precio_Entrada: int, Visitantes_Millones: int]



### 3.-Filtrado


```python
from pyspark.sql.functions import col, lit
df_filtered = df_es.filter((col("Es_UNESCO") == "Yes") & (col("Precio_Entrada") <= 20))
df_filtered.show(5)
```

                                                                                    

    +--------------------+-------+---------+--------------+-------------------+
    |               Lugar|Country|Es_UNESCO|Precio_Entrada|Visitantes_Millones|
    +--------------------+-------+---------+--------------+-------------------+
    | Great Wall of China|  China|      Yes|            10|                 10|
    |           Taj Mahal|  India|      Yes|            15|               NULL|
    |           Colosseum|  Italy|      Yes|            18|               NULL|
    |      Forbidden City|  China|      Yes|             8|                  9|
    |Notre-Dame Cathedral| France|      Yes|             0|                 13|
    +--------------------+-------+---------+--------------+-------------------+
    only showing top 5 rows
    


## Dataset 3: Registro turístico de Castilla y León


```python
schema = StructType([
    StructField("establecimiento", StringType(), False),
    StructField("n_registro", StringType(), False),
    StructField("codigo", StringType(), True),
    StructField("tipo", StringType(), True),
    StructField("categoria", StringType(), True),
    StructField("especialidades", StringType(), True),
    StructField("clase", StringType(), True),
    StructField("nombre", StringType(), False),
    StructField("direccion", StringType(), False),
    StructField("c_postal", StringType(), False),
    StructField("provincia", StringType(), False),
    StructField("municipio", StringType(), True),
    StructField("localidad", StringType(), True),
    StructField("nucleo", StringType(), True),
    StructField("telefono_1", StringType(), True),
    StructField("telefono_2", StringType(), True),
    StructField("telefono_3", StringType(), True),
    StructField("email", StringType(), True),
    StructField("web", StringType(), True),
    StructField("q_calidad", StringType(), True),
    StructField("posada_real", StringType(), True),
    StructField("plazas", StringType(), True),
    StructField("gps_longitud", DoubleType(), True),
    StructField("gps_latitud", DoubleType(), True),
    StructField("accesible_a_personas_con_discapacidad", StringType(), True),
    StructField("column_27", StringType(), True),
    StructField("posicion", StringType(), True),
])
```


```python
df = (
    spark.read
        .format("csv")
        .schema(schema)
        .option("delimiter", ";")
        .option("header", "true")
        .option("quote", "")
        .option("escape", "\\")
        .option("multiLine", "true")   
        .option("emptyValue", None)    
        .option("nullValue", "NULL")
        .load("/workspace/pr0501/registro-de-turismo-de-castilla-y-leon.csv")
)
```

### 1.-Selección y saneamiento


```python
df_contactos = df.select("nombre", "tipo", "provincia", "web", "email")
df_contactos
```




    DataFrame[nombre: string, tipo: string, provincia: string, web: string, email: string]



### 2.-Renombrado estándar


```python
df_renombrado = df_contactos \
    .withColumnRenamed("nombre", "nombre_establecimiento") \
    .withColumnRenamed("tipo", "categoria_actividad") \
    .withColumnRenamed("web", "sitio_web") \
    .withColumnRenamed("email", "correo_electronico")
df_renombrado
```




    DataFrame[nombre_establecimiento: string, categoria_actividad: string, provincia: string, sitio_web: string, correo_electronico: string]



### 3.-Filtrado de texto


```python
df_filtrado = df_renombrado.where((col("provincia") == "Burgos") & (col("categoria_actividad").like("%Bodegas%")) & (col("web").isNotNull()))
df_filtrado.show(5)
```

    +----------------------+--------------------+---------+--------------------+--------------------+
    |nombre_establecimiento| categoria_actividad|provincia|           sitio_web|  correo_electronico|
    +----------------------+--------------------+---------+--------------------+--------------------+
    |        BODEGAS TARSUS|g - Bodegas y los...|   Burgos|  www.tarsusvino.com|                NULL|
    |  BODEGAS DOMINIO D...|g - Bodegas y los...|   Burgos|www.dominiodecair...|bodegas@dominiode...|
    |    TERRITORIO LUTHIER|g - Bodegas y los...|   Burgos|territorioluthier...|luthier@territori...|
    |    BODEGA COVARRUBIAS|g - Bodegas y los...|   Burgos| http://valdable.com|   info@valdable.com|
    |  BODEGAS PASCUAL,"...|g - Bodegas y los...|   Burgos|222.bodegaspascua...|export@bodegaspas...|
    +----------------------+--------------------+---------+--------------------+--------------------+
    only showing top 5 rows
    


                                                                                    
