# PR0504. Limpieza de datos sobre dataset de lugares famosos


```python
from pyspark.sql.types import IntegerType, StructType, StructField, StringType, DoubleType
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
```


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
        .load("/workspace/pr0504/world_famous_places_2024.csv")
)
df.show(5)
```

    Setting default log level to "WARN".
    To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
    26/01/29 09:24:24 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
                                                                                    

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
    


## Ejercicio 1: Generación de códigos SKUs


```python
from pyspark.sql.functions import substring, concat_ws, col, split
df = (
    df
        .withColumn("PKU", concat_ws("_", substring(col("Country"), 0, 3), substring(col("City"), 0, 3), split(split(col("Type"), "/")[0], " ")[0]))
)

df.show(5)
```

    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+----------------+
    |         Place_Name|      Country|            City|Annual_Visitors_Millions|              Type|UNESCO_World_Heritage|      Year_Build|Entry_Fee_USD| Best_Visit_Month|        Region|Tourism_Revenue_Million_USD|Average_Visit_Duration_Hours|          Famous_For|             PKU|
    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+----------------+
    |       Eiffel Tower|       France|           Paris|                       7|    Monument/Tower|                   No|            1889|           35|May-June/Sept-Oct|Western Europe|                         95|                         2.5|Iconic iron latti...|Fra_Par_Monument|
    |       Times Square|United States|   New York City|                      50|    Urban Landmark|                   No|            1904|            0|Apr-June/Sept-Nov| North America|                         70|                         1.5|Bright lights, Br...|   Uni_New_Urban|
    |      Louvre Museum|       France|           Paris|                    NULL|            Museum|                  Yes|            1793|           22|        Oct-March|Western Europe|                        120|                         4.0|World's most visi...|  Fra_Par_Museum|
    |Great Wall of China|        China|Beijing/Multiple|                      10| Historic Monument|                  Yes|220 BC - 1644 AD|           10| Apr-May/Sept-Oct|     East Asia|                        180|                         4.0|Ancient defensive...|Chi_Bei_Historic|
    |          Taj Mahal|        India|            Agra|                    NULL|Monument/Mausoleum|                  Yes|            1653|           15|        Oct-March|    South Asia|                         65|                         2.0|White marble maus...|Ind_Agr_Monument|
    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+----------------+
    only showing top 5 rows
    


## Ejercicio 2: Ajuste de precios y tiempos


```python
from pyspark.sql.functions import ceil, log10, least, lit
df = (
    df 
        .withColumn("Duracion_Techo", ceil(col("Average_Visit_Duration_Hours")))
        .withColumn("Log_Ingresos", log10(col("Tourism_Revenue_Million_USD")))
        .withColumn("Mejor_Oferta", least(col("Entry_Fee_USD"), lit(20)))
)
df.show(5)
```

    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+----------------+--------------+------------------+------------+
    |         Place_Name|      Country|            City|Annual_Visitors_Millions|              Type|UNESCO_World_Heritage|      Year_Build|Entry_Fee_USD| Best_Visit_Month|        Region|Tourism_Revenue_Million_USD|Average_Visit_Duration_Hours|          Famous_For|             PKU|Duracion_Techo|      Log_Ingresos|Mejor_Oferta|
    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+----------------+--------------+------------------+------------+
    |       Eiffel Tower|       France|           Paris|                       7|    Monument/Tower|                   No|            1889|           35|May-June/Sept-Oct|Western Europe|                         95|                         2.5|Iconic iron latti...|Fra_Par_Monument|             3|1.9777236052888478|          20|
    |       Times Square|United States|   New York City|                      50|    Urban Landmark|                   No|            1904|            0|Apr-June/Sept-Nov| North America|                         70|                         1.5|Bright lights, Br...|   Uni_New_Urban|             2| 1.845098040014257|           0|
    |      Louvre Museum|       France|           Paris|                    NULL|            Museum|                  Yes|            1793|           22|        Oct-March|Western Europe|                        120|                         4.0|World's most visi...|  Fra_Par_Museum|             4|2.0791812460476247|          20|
    |Great Wall of China|        China|Beijing/Multiple|                      10| Historic Monument|                  Yes|220 BC - 1644 AD|           10| Apr-May/Sept-Oct|     East Asia|                        180|                         4.0|Ancient defensive...|Chi_Bei_Historic|             4| 2.255272505103306|          10|
    |          Taj Mahal|        India|            Agra|                    NULL|Monument/Mausoleum|                  Yes|            1653|           15|        Oct-March|    South Asia|                         65|                         2.0|White marble maus...|Ind_Agr_Monument|             2|1.8129133566428555|          15|
    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+----------------+--------------+------------------+------------+
    only showing top 5 rows
    


## Ejercicio 3: Limpieza de texto


```python
from pyspark.sql.functions import substring, regexp_replace
df = (
    df 
        .withColumn("Desc_Corta", substring(col("Famous_For"), 1, 15))
        .withColumn("Ciudad_Limpia", regexp_replace(col("City"), "New York City", "NYC"))
)
df.show(5)
```

    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+----------------+--------------+------------------+------------+---------------+----------------+
    |         Place_Name|      Country|            City|Annual_Visitors_Millions|              Type|UNESCO_World_Heritage|      Year_Build|Entry_Fee_USD| Best_Visit_Month|        Region|Tourism_Revenue_Million_USD|Average_Visit_Duration_Hours|          Famous_For|             PKU|Duracion_Techo|      Log_Ingresos|Mejor_Oferta|     Desc_Corta|   Ciudad_Limpia|
    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+----------------+--------------+------------------+------------+---------------+----------------+
    |       Eiffel Tower|       France|           Paris|                       7|    Monument/Tower|                   No|            1889|           35|May-June/Sept-Oct|Western Europe|                         95|                         2.5|Iconic iron latti...|Fra_Par_Monument|             3|1.9777236052888478|          20|Iconic iron lat|           Paris|
    |       Times Square|United States|   New York City|                      50|    Urban Landmark|                   No|            1904|            0|Apr-June/Sept-Nov| North America|                         70|                         1.5|Bright lights, Br...|   Uni_New_Urban|             2| 1.845098040014257|           0|Bright lights, |             NYC|
    |      Louvre Museum|       France|           Paris|                    NULL|            Museum|                  Yes|            1793|           22|        Oct-March|Western Europe|                        120|                         4.0|World's most visi...|  Fra_Par_Museum|             4|2.0791812460476247|          20|World's most vi|           Paris|
    |Great Wall of China|        China|Beijing/Multiple|                      10| Historic Monument|                  Yes|220 BC - 1644 AD|           10| Apr-May/Sept-Oct|     East Asia|                        180|                         4.0|Ancient defensive...|Chi_Bei_Historic|             4| 2.255272505103306|          10|Ancient defensi|Beijing/Multiple|
    |          Taj Mahal|        India|            Agra|                    NULL|Monument/Mausoleum|                  Yes|            1653|           15|        Oct-March|    South Asia|                         65|                         2.0|White marble maus...|Ind_Agr_Monument|             2|1.8129133566428555|          15|White marble ma|            Agra|
    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+----------------+--------------+------------------+------------+---------------+----------------+
    only showing top 5 rows
    


## Ejercicio 4: Gestión de fechas de campaña


```python
from pyspark.sql.functions import to_date, date_add, datediff, concat
df = (
    df
        .withColumn("Inicio_Campana", to_date(lit("2024-06-01")))
        .withColumn("Fin_Campana", date_add(col("Inicio_Campana"), 90))
        .withColumn("Dias_Hasta_Fin", datediff(col("Fin_Campana"), to_date(concat(col("Year_Build"), lit("-01-01")))))
)
df.show(5)
```

    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+----------------+--------------+------------------+------------+---------------+----------------+--------------+-----------+--------------+
    |         Place_Name|      Country|            City|Annual_Visitors_Millions|              Type|UNESCO_World_Heritage|      Year_Build|Entry_Fee_USD| Best_Visit_Month|        Region|Tourism_Revenue_Million_USD|Average_Visit_Duration_Hours|          Famous_For|             PKU|Duracion_Techo|      Log_Ingresos|Mejor_Oferta|     Desc_Corta|   Ciudad_Limpia|Inicio_Campana|Fin_Campana|Dias_Hasta_Fin|
    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+----------------+--------------+------------------+------------+---------------+----------------+--------------+-----------+--------------+
    |       Eiffel Tower|       France|           Paris|                       7|    Monument/Tower|                   No|            1889|           35|May-June/Sept-Oct|Western Europe|                         95|                         2.5|Iconic iron latti...|Fra_Par_Monument|             3|1.9777236052888478|          20|Iconic iron lat|           Paris|    2024-06-01| 2024-08-30|         49549|
    |       Times Square|United States|   New York City|                      50|    Urban Landmark|                   No|            1904|            0|Apr-June/Sept-Nov| North America|                         70|                         1.5|Bright lights, Br...|   Uni_New_Urban|             2| 1.845098040014257|           0|Bright lights, |             NYC|    2024-06-01| 2024-08-30|         44072|
    |      Louvre Museum|       France|           Paris|                    NULL|            Museum|                  Yes|            1793|           22|        Oct-March|Western Europe|                        120|                         4.0|World's most visi...|  Fra_Par_Museum|             4|2.0791812460476247|          20|World's most vi|           Paris|    2024-06-01| 2024-08-30|         84612|
    |Great Wall of China|        China|Beijing/Multiple|                      10| Historic Monument|                  Yes|220 BC - 1644 AD|           10| Apr-May/Sept-Oct|     East Asia|                        180|                         4.0|Ancient defensive...|Chi_Bei_Historic|             4| 2.255272505103306|          10|Ancient defensi|Beijing/Multiple|    2024-06-01| 2024-08-30|          NULL|
    |          Taj Mahal|        India|            Agra|                    NULL|Monument/Mausoleum|                  Yes|            1653|           15|        Oct-March|    South Asia|                         65|                         2.0|White marble maus...|Ind_Agr_Monument|             2|1.8129133566428555|          15|White marble ma|            Agra|    2024-06-01| 2024-08-30|        135746|
    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+----------------+--------------+------------------+------------+---------------+----------------+--------------+-----------+--------------+
    only showing top 5 rows
    

