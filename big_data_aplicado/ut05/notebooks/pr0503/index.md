# PR0503. Limpieza de datos sobre el dataset de cultivos


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
    StructField("Fertilizer_Used_kg", DoubleType(), False),
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
     StructField('Fertilizer_Used_kg', DoubleType(), False),
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

## 1. Creación de un ID único


```python
from pyspark.sql.functions import col, concat_ws, lit, split, upper, lpad
df_eng = df.withColumn("Crop_ID", concat_ws("-", lit("CODIGO_"), lpad(split(col("Region"), "_")[1], 3, "X"), upper(col("Crop"))))
df_eng.show(5)
```

    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------------+
    |  Crop|  Region|Soil_Type|Soil_pH|Rainfall_mm|Temperature_C|Humidity_pct|Fertilizer_Used_kg|Irrigation|Pesticides_Used_kg|Planting_Density|Previous_Crop|Yield_ton_per_ha|           Crop_ID|
    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------------+
    | Maize|Region_C|    Sandy|   7.01|     1485.4|         19.7|        40.3|             105.1|      Drip|              10.2|            23.2|         Rice|          101.48| CODIGO_-XXC-MAIZE|
    |Barley|Region_D|     Loam|   5.79|      399.4|         29.1|        55.4|             221.8| Sprinkler|              35.5|             7.4|       Barley|          127.39|CODIGO_-XXD-BARLEY|
    |  Rice|Region_C|     Clay|   7.24|      980.9|         30.5|        74.4|              61.2| Sprinkler|              40.0|             5.1|        Wheat|           68.99|  CODIGO_-XXC-RICE|
    | Maize|Region_D|     Loam|   6.79|     1054.3|         26.4|        62.0|             257.8|      Drip|              42.7|            23.7|         None|          169.06| CODIGO_-XXD-MAIZE|
    | Maize|Region_D|    Sandy|   5.96|      744.6|         20.4|        70.9|             195.8|      Drip|              25.5|            15.6|        Maize|          118.71| CODIGO_-XXD-MAIZE|
    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------------+
    only showing top 5 rows
    


## 2. Transformación matemática


```python
from pyspark.sql.functions import log10, round
df_eng = (
    df_eng 
    .withColumn("Log_Rainfall", log10(col("Rainfall_mm") + 1))
    .withColumn("Yield_ton_per_ha", round(col("Yield_ton_per_ha"), 2))
        )
df_eng.show(5)
```

    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------------+------------------+
    |  Crop|  Region|Soil_Type|Soil_pH|Rainfall_mm|Temperature_C|Humidity_pct|Fertilizer_Used_kg|Irrigation|Pesticides_Used_kg|Planting_Density|Previous_Crop|Yield_ton_per_ha|           Crop_ID|      Log_Rainfall|
    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------------+------------------+
    | Maize|Region_C|    Sandy|   7.01|     1485.4|         19.7|        40.3|             105.1|      Drip|              10.2|            23.2|         Rice|          101.48| CODIGO_-XXC-MAIZE|3.1721356966495664|
    |Barley|Region_D|     Loam|   5.79|      399.4|         29.1|        55.4|             221.8| Sprinkler|              35.5|             7.4|       Barley|          127.39|CODIGO_-XXD-BARLEY| 2.602494068807281|
    |  Rice|Region_C|     Clay|   7.24|      980.9|         30.5|        74.4|              61.2| Sprinkler|              40.0|             5.1|        Wheat|           68.99|  CODIGO_-XXC-RICE|2.9920672600276665|
    | Maize|Region_D|     Loam|   6.79|     1054.3|         26.4|        62.0|             257.8|      Drip|              42.7|            23.7|         None|          169.06| CODIGO_-XXD-MAIZE|3.0233759381395626|
    | Maize|Region_D|    Sandy|   5.96|      744.6|         20.4|        70.9|             195.8|      Drip|              25.5|            15.6|        Maize|          118.71| CODIGO_-XXD-MAIZE| 2.872505899345925|
    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------------+------------------+
    only showing top 5 rows
    


## 3. Comparación de insumos


```python
from pyspark.sql.functions import greatest
df_eng = (
    df_eng
        .withColumn("Max_Quimico_kg", greatest(col("Fertilizer_Used_kg"), col("Pesticides_Used_kg")))
)
df_eng.show(5)
```

    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------------+------------------+--------------+
    |  Crop|  Region|Soil_Type|Soil_pH|Rainfall_mm|Temperature_C|Humidity_pct|Fertilizer_Used_kg|Irrigation|Pesticides_Used_kg|Planting_Density|Previous_Crop|Yield_ton_per_ha|           Crop_ID|      Log_Rainfall|Max_Quimico_kg|
    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------------+------------------+--------------+
    | Maize|Region_C|    Sandy|   7.01|     1485.4|         19.7|        40.3|             105.1|      Drip|              10.2|            23.2|         Rice|          101.48| CODIGO_-XXC-MAIZE|3.1721356966495664|         105.1|
    |Barley|Region_D|     Loam|   5.79|      399.4|         29.1|        55.4|             221.8| Sprinkler|              35.5|             7.4|       Barley|          127.39|CODIGO_-XXD-BARLEY| 2.602494068807281|         221.8|
    |  Rice|Region_C|     Clay|   7.24|      980.9|         30.5|        74.4|              61.2| Sprinkler|              40.0|             5.1|        Wheat|           68.99|  CODIGO_-XXC-RICE|2.9920672600276665|          61.2|
    | Maize|Region_D|     Loam|   6.79|     1054.3|         26.4|        62.0|             257.8|      Drip|              42.7|            23.7|         None|          169.06| CODIGO_-XXD-MAIZE|3.0233759381395626|         257.8|
    | Maize|Region_D|    Sandy|   5.96|      744.6|         20.4|        70.9|             195.8|      Drip|              25.5|            15.6|        Maize|          118.71| CODIGO_-XXD-MAIZE| 2.872505899345925|         195.8|
    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------------+------------------+--------------+
    only showing top 5 rows
    


## 4. Simulación de fechas


```python
from pyspark.sql.functions import to_date, date_add, month, lit, date_format
df_eng = (
    df_eng
        .withColumn("Fecha_Siembra", to_date(lit("2023-04-01"), "yyyy-MM-dd"))
        .withColumn("Fecha_Estimada_Cosecha", date_add(col("Fecha_Siembra"), 150))
        .withColumn("Mes_Cosecha", date_format(to_date(month(col("Fecha_Estimada_Cosecha")).cast("string"), "M"), "MMMM"))
)
df_eng.show(5)
```

    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------------+------------------+--------------+-------------+----------------------+-----------+
    |  Crop|  Region|Soil_Type|Soil_pH|Rainfall_mm|Temperature_C|Humidity_pct|Fertilizer_Used_kg|Irrigation|Pesticides_Used_kg|Planting_Density|Previous_Crop|Yield_ton_per_ha|           Crop_ID|      Log_Rainfall|Max_Quimico_kg|Fecha_Siembra|Fecha_Estimada_Cosecha|Mes_Cosecha|
    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------------+------------------+--------------+-------------+----------------------+-----------+
    | Maize|Region_C|    Sandy|   7.01|     1485.4|         19.7|        40.3|             105.1|      Drip|              10.2|            23.2|         Rice|          101.48| CODIGO_-XXC-MAIZE|3.1721356966495664|         105.1|   2023-04-01|            2023-08-29|     August|
    |Barley|Region_D|     Loam|   5.79|      399.4|         29.1|        55.4|             221.8| Sprinkler|              35.5|             7.4|       Barley|          127.39|CODIGO_-XXD-BARLEY| 2.602494068807281|         221.8|   2023-04-01|            2023-08-29|     August|
    |  Rice|Region_C|     Clay|   7.24|      980.9|         30.5|        74.4|              61.2| Sprinkler|              40.0|             5.1|        Wheat|           68.99|  CODIGO_-XXC-RICE|2.9920672600276665|          61.2|   2023-04-01|            2023-08-29|     August|
    | Maize|Region_D|     Loam|   6.79|     1054.3|         26.4|        62.0|             257.8|      Drip|              42.7|            23.7|         None|          169.06| CODIGO_-XXD-MAIZE|3.0233759381395626|         257.8|   2023-04-01|            2023-08-29|     August|
    | Maize|Region_D|    Sandy|   5.96|      744.6|         20.4|        70.9|             195.8|      Drip|              25.5|            15.6|        Maize|          118.71| CODIGO_-XXD-MAIZE| 2.872505899345925|         195.8|   2023-04-01|            2023-08-29|     August|
    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+------------------+------------------+--------------+-------------+----------------------+-----------+
    only showing top 5 rows
    

