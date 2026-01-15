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

    Setting default log level to "WARN".
    To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
    26/01/15 11:00:21 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable



```python
df.printSchema()
df.show(5)
```

    root
     |-- Crop: string (nullable = true)
     |-- Region: string (nullable = true)
     |-- Soil_Type: string (nullable = true)
     |-- Soil_pH: double (nullable = true)
     |-- Rainfall_mm: double (nullable = true)
     |-- Temperature_C: double (nullable = true)
     |-- Humidity_pct: double (nullable = true)
     |-- Fertilizar_Used_kg: double (nullable = true)
     |-- Irrigation: string (nullable = true)
     |-- Pesticides_Used_kg: double (nullable = true)
     |-- Planting_Density: double (nullable = true)
     |-- Previous_Crop: string (nullable = true)
     |-- Yield_ton_per_ha: double (nullable = true)
    


                                                                                    

    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+
    |  Crop|  Region|Soil_Type|Soil_pH|Rainfall_mm|Temperature_C|Humidity_pct|Fertilizar_Used_kg|Irrigation|Pesticides_Used_kg|Planting_Density|Previous_Crop|Yield_ton_per_ha|
    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+
    | Maize|Region_C|    Sandy|   7.01|     1485.4|         19.7|        40.3|             105.1|      Drip|              10.2|            23.2|         Rice|          101.48|
    |Barley|Region_D|     Loam|   5.79|      399.4|         29.1|        55.4|             221.8| Sprinkler|              35.5|             7.4|       Barley|          127.39|
    |  Rice|Region_C|     Clay|   7.24|      980.9|         30.5|        74.4|              61.2| Sprinkler|              40.0|             5.1|        Wheat|           68.99|
    | Maize|Region_D|     Loam|   6.79|     1054.3|         26.4|        62.0|             257.8|      Drip|              42.7|            23.7|         None|          169.06|
    | Maize|Region_D|    Sandy|   5.96|      744.6|         20.4|        70.9|             195.8|      Drip|              25.5|            15.6|        Maize|          118.71|
    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+
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


```python
df.printSchema()
df.show(5)
```

    root
     |-- Place_Name: string (nullable = true)
     |-- Country: string (nullable = true)
     |-- City: string (nullable = true)
     |-- Annual_Visitors_Millions: integer (nullable = true)
     |-- Type: string (nullable = true)
     |-- UNESCO_World_Heritage: string (nullable = true)
     |-- Year_Build: string (nullable = true)
     |-- Entry_Fee_USD: integer (nullable = true)
     |-- Best_Visit_Month: string (nullable = true)
     |-- Region: string (nullable = true)
     |-- Tourism_Revenue_Million_USD: integer (nullable = true)
     |-- Average_Visit_Duration_Hours: double (nullable = true)
     |-- Famous_For: string (nullable = true)
    
    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
    |         Place_Name|      Country|            City|Annual_Visitors_Millions|              Type|UNESCO_World_Heritage|      Year_Build|Entry_Fee_USD| Best_Visit_Month|        Region|Tourism_Revenue_Million_USD|Average_Visit_Duration_Hours|          Famous_For|
    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
    |       Eiffel Tower|       France|           Paris|                       7|    Monument/Tower|                   No|            1889|           35|May-June/Sept-Oct|Western Europe|                         95|                         2.5|Iconic iron latti...|
    |       Times Square|United States|   New York City|                      50|    Urban Landmark|                   No|            1904|            0|Apr-June/Sept-Nov| North America|                         70|                         1.5|Bright lights, Br...|
    |      Louvre Museum|       France|           Paris|                    NULL|            Museum|                  Yes|            1793|           22|        Oct-March|Western Europe|                        120|                         4.0|World's most visi...|
    |Great Wall of China|        China|Beijing/Multiple|                      10| Historic Monument|                  Yes|220 BC - 1644 AD|           10| Apr-May/Sept-Oct|     East Asia|                        180|                         4.0|Ancient defensive...|
    |          Taj Mahal|        India|            Agra|                    NULL|Monument/Mausoleum|                  Yes|            1653|           15|        Oct-March|    South Asia|                         65|                         2.0|White marble maus...|
    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
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
    StructField("porvincia", StringType(), False),
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


```python
df.printSchema()
df.show(5)
```

    root
     |-- establecimiento: string (nullable = true)
     |-- n_registro: string (nullable = true)
     |-- codigo: string (nullable = true)
     |-- tipo: string (nullable = true)
     |-- categoria: string (nullable = true)
     |-- especialidades: string (nullable = true)
     |-- clase: string (nullable = true)
     |-- nombre: string (nullable = true)
     |-- direccion: string (nullable = true)
     |-- c_postal: string (nullable = true)
     |-- porvincia: string (nullable = true)
     |-- municipio: string (nullable = true)
     |-- localidad: string (nullable = true)
     |-- nucleo: string (nullable = true)
     |-- telefono_1: string (nullable = true)
     |-- telefono_2: string (nullable = true)
     |-- telefono_3: string (nullable = true)
     |-- email: string (nullable = true)
     |-- web: string (nullable = true)
     |-- q_calidad: string (nullable = true)
     |-- posada_real: string (nullable = true)
     |-- plazas: string (nullable = true)
     |-- gps_longitud: double (nullable = true)
     |-- gps_latitud: double (nullable = true)
     |-- accesible_a_personas_con_discapacidad: string (nullable = true)
     |-- column_27: string (nullable = true)
     |-- posicion: string (nullable = true)
    


    26/01/15 11:00:25 WARN SparkStringUtils: Truncated the string representation of a plan since it was too large. This behavior can be adjusted by setting 'spark.sql.debug.maxToStringFields'.


    +--------------------+----------+------+--------------------+---------------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    |     establecimiento|n_registro|codigo|                tipo|      categoria|especialidades|clase|              nombre|           direccion|c_postal|porvincia|municipio|      localidad|         nucleo|telefono_1|telefono_2|telefono_3|               email|                 web|q_calidad|posada_real|plazas|gps_longitud|gps_latitud|accesible_a_personas_con_discapacidad|column_27|            posicion|
    +--------------------+----------+------+--------------------+---------------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    |      Turismo Activo| 47/000047|  NULL|Profesional de Tu...|           NULL|          NULL| NULL|BERNARDO MORO MEN...|Calle Rio Somiedo...|   33840| Asturias|  Somiedo|POLA DE SOMIEDO|POLA DE SOMIEDO| 616367277|      NULL|      NULL|bernardomoro@hotm...|                NULL|     NULL|       NULL|  NULL|        NULL|       NULL|                                 NULL|     NULL|                NULL|
    |Alojam. Turismo R...| 05/000788|  NULL|Casa Rural de Alq...|    3 Estrellas|          NULL| NULL|        LA SASTRERÍA|Calle VEINTIOCHO ...|   05296|    Ávila|  Adanero|        ADANERO|        ADANERO| 920307158| 606945069| 609289521|                NULL|www.lasastreriade...|     NULL|       NULL|     6|        NULL|       NULL|                                 NULL|     NULL|                NULL|
    |Alojam. Turismo R...| 05/000696|  NULL|Casa Rural de Alq...|    4 Estrellas|          NULL| NULL|         LAS HAZANAS|       Plaza MAYOR 4|   05296|    Ávila|  Adanero|        ADANERO|        ADANERO| 655099974|      NULL|      NULL|lashazanas@hotmai...|                NULL|     NULL|       NULL|     8|  -4.6033331| 40.9438881|                                 NULL|     NULL|40.9438881," -4.6...|
    |Alojam. Turismo R...| 05/001050|  NULL|Casa Rural de Alq...|    4 Estrellas|          NULL| NULL| LA CASITA DEL PAJAR|   Plaza MAYOR 4   B|   05296|    Ávila|  Adanero|        ADANERO|        ADANERO| 655099974|      NULL|      NULL|lashazanas@hotmai...|                NULL|     NULL|       NULL|     2|  -4.6033333| 40.9438889|                                 NULL|     NULL|40.9438889," -4.6...|
    |               Bares| 05/002525|  NULL|                 Bar|Categoría única|          NULL| NULL|            MARACANA|Calle 28 DE JUNIO...|   05296|    Ávila|  Adanero|        ADANERO|        ADANERO| 666389333|      NULL|      NULL|emo123anatoliev@g...|                NULL|     NULL|       NULL|    42|        NULL|       NULL|                                   Si|     NULL|                NULL|
    +--------------------+----------+------+--------------------+---------------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    only showing top 5 rows
    


    26/01/15 11:00:40 WARN GarbageCollectionMetrics: To enable non-built-in garbage collector(s) List(G1 Concurrent GC), users should configure it(them) to spark.eventLog.gcMetrics.youngGenerationGarbageCollectors or spark.eventLog.gcMetrics.oldGenerationGarbageCollectors

