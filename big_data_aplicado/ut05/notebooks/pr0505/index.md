# PR0505. Análisis de estadísticas en dataset


```python
from pyspark.sql.types import StringType, IntegerType, DoubleType, StructType, StructField 
schema = StructType([
    StructField("Index", IntegerType(), False),
    StructField("Title", StringType(), False),
    StructField("Description", StringType(), False),
    StructField("Amount(in rupees)", StringType(), False),
    StructField("Price (in rupees)", IntegerType(), True),
    StructField("location", StringType(), False), 
    StructField("Carpet Area", StringType(), False),
    StructField("Status", StringType(), False),
    StructField("Floor", StringType(), False),
    StructField("Transaction", StringType(), False),
    StructField("Furnishing", StringType(), False),
    StructField("facing", StringType(), True),
    StructField("overlooking", StringType(), True),
    StructField("Society", StringType(), True),
    StructField("Bathroom", IntegerType(), False),
    StructField("Balcony", IntegerType(), True),
    StructField("Car Parking", StringType(), True),
    StructField("Ownership", StringType(), True),
    StructField("Super Area", StringType(), True),
    StructField("Dimensions", StringType(), True),
    StructField("Plot Area", StringType(), True),
])
```


```python
from pyspark.sql import SparkSession

spark = (
    SparkSession
        .builder
        .appName("Estadisticas")
        .master("spark://spark-master:7077")
        .getOrCreate()
)

df = (
    spark
        .read
        .format("csv")
        .schema(schema)
        .option("header", "true")
        .load("/workspace/pr0505/house_prices.csv")
)

df.show(5)
```

    +-----+--------------------+--------------------+-----------------+-----------------+--------+-----------+-------------+------------+-----------+--------------+------+--------------------+--------------------+--------+-------+-----------+--------------------+----------+----------+---------+
    |Index|               Title|         Description|Amount(in rupees)|Price (in rupees)|location|Carpet Area|       Status|       Floor|Transaction|    Furnishing|facing|         overlooking|             Society|Bathroom|Balcony|Car Parking|           Ownership|Super Area|Dimensions|Plot Area|
    +-----+--------------------+--------------------+-----------------+-----------------+--------+-----------+-------------+------------+-----------+--------------+------+--------------------+--------------------+--------+-------+-----------+--------------------+----------+----------+---------+
    |    0|1 BHK Ready to Oc...|Bhiwandi, Thane h...|          42 Lac |             6000|   thane|   500 sqft|Ready to Move|10 out of 11|     Resale|   Unfurnished|  NULL|                NULL|Srushti Siddhi Ma...|       1|      2|       NULL|                NULL|      NULL|      NULL|     NULL|
    |    1|2 BHK Ready to Oc...|One can find this...|          98 Lac |            13799|   thane|   473 sqft|Ready to Move| 3 out of 22|     Resale|Semi-Furnished|  East|         Garden/Park|         Dosti Vihar|       2|   NULL|     1 Open|            Freehold|      NULL|      NULL|     NULL|
    |    2|2 BHK Ready to Oc...|Up for immediate ...|         1.40 Cr |            17500|   thane|   779 sqft|Ready to Move|10 out of 29|     Resale|   Unfurnished|  East|         Garden/Park|Sunrise by Kalpataru|       2|   NULL|  1 Covered|            Freehold|      NULL|      NULL|     NULL|
    |    3|1 BHK Ready to Oc...|This beautiful 1 ...|          25 Lac |             NULL|   thane|   530 sqft|Ready to Move|  1 out of 3|     Resale|   Unfurnished|  NULL|                NULL|                NULL|       1|      1|       NULL|                NULL|      NULL|      NULL|     NULL|
    |    4|2 BHK Ready to Oc...|This lovely 2 BHK...|         1.60 Cr |            18824|   thane|   635 sqft|Ready to Move|20 out of 42|     Resale|   Unfurnished|  West|Garden/Park, Main...|TenX Habitat Raym...|       2|   NULL|  1 Covered|Co-operative Society|      NULL|      NULL|     NULL|
    +-----+--------------------+--------------------+-----------------+-----------------+--------+-----------+-------------+------------+-----------+--------------+------+--------------------+--------------------+--------+-------+-----------+--------------------+----------+----------+---------+
    only showing top 5 rows
    


## 1. Objetivos de ingeniería de datos (ETL)
### 1.1. Estandarización monetaria (de INR a USD)


```python
from pyspark.sql.functions import col, when, split
df = (
    df.withColumn("Amount_USD",
        when(split(col("Amount(in rupees)"), " ").getItem(1) == "Lac", split(col("Amount(in rupees)"), " ").getItem(0).cast("int") * 100_000 * 0.012)
        .otherwise(split(col("Amount(in rupees)"), " ").getItem(0).cast("float") * 10_000_000 * 0.012)
     )
)
df.show(5)
```

    +-----+--------------------+--------------------+-----------------+-----------------+--------+-----------+-------------+------------+-----------+--------------+------+--------------------+--------------------+--------+-------+-----------+--------------------+----------+----------+---------+----------+
    |Index|               Title|         Description|Amount(in rupees)|Price (in rupees)|location|Carpet Area|       Status|       Floor|Transaction|    Furnishing|facing|         overlooking|             Society|Bathroom|Balcony|Car Parking|           Ownership|Super Area|Dimensions|Plot Area|Amount_USD|
    +-----+--------------------+--------------------+-----------------+-----------------+--------+-----------+-------------+------------+-----------+--------------+------+--------------------+--------------------+--------+-------+-----------+--------------------+----------+----------+---------+----------+
    |    0|1 BHK Ready to Oc...|Bhiwandi, Thane h...|          42 Lac |             6000|   thane|   500 sqft|Ready to Move|10 out of 11|     Resale|   Unfurnished|  NULL|                NULL|Srushti Siddhi Ma...|       1|      2|       NULL|                NULL|      NULL|      NULL|     NULL|   50400.0|
    |    1|2 BHK Ready to Oc...|One can find this...|          98 Lac |            13799|   thane|   473 sqft|Ready to Move| 3 out of 22|     Resale|Semi-Furnished|  East|         Garden/Park|         Dosti Vihar|       2|   NULL|     1 Open|            Freehold|      NULL|      NULL|     NULL|  117600.0|
    |    2|2 BHK Ready to Oc...|Up for immediate ...|         1.40 Cr |            17500|   thane|   779 sqft|Ready to Move|10 out of 29|     Resale|   Unfurnished|  East|         Garden/Park|Sunrise by Kalpataru|       2|   NULL|  1 Covered|            Freehold|      NULL|      NULL|     NULL|  168000.0|
    |    3|1 BHK Ready to Oc...|This beautiful 1 ...|          25 Lac |             NULL|   thane|   530 sqft|Ready to Move|  1 out of 3|     Resale|   Unfurnished|  NULL|                NULL|                NULL|       1|      1|       NULL|                NULL|      NULL|      NULL|     NULL|   30000.0|
    |    4|2 BHK Ready to Oc...|This lovely 2 BHK...|         1.60 Cr |            18824|   thane|   635 sqft|Ready to Move|20 out of 42|     Resale|   Unfurnished|  West|Garden/Park, Main...|TenX Habitat Raym...|       2|   NULL|  1 Covered|Co-operative Society|      NULL|      NULL|     NULL|  192000.0|
    +-----+--------------------+--------------------+-----------------+-----------------+--------+-----------+-------------+------------+-----------+--------------+------+--------------------+--------------------+--------+-------+-----------+--------------------+----------+----------+---------+----------+
    only showing top 5 rows
    


### 1.2. Estandarización de superficie


```python
df = (
    df
        .withColumn("Carpet Area", split(col("Carpet Area"), " ").getField(0).cast("float") * 0.0929)
)
df.show(5)
```

    +-----+--------------------+--------------------+-----------------+-----------------+--------+------------------+-------------+------------+-----------+--------------+------+--------------------+--------------------+--------+-------+-----------+--------------------+----------+----------+---------+----------+
    |Index|               Title|         Description|Amount(in rupees)|Price (in rupees)|location|       Carpet Area|       Status|       Floor|Transaction|    Furnishing|facing|         overlooking|             Society|Bathroom|Balcony|Car Parking|           Ownership|Super Area|Dimensions|Plot Area|Amount_USD|
    +-----+--------------------+--------------------+-----------------+-----------------+--------+------------------+-------------+------------+-----------+--------------+------+--------------------+--------------------+--------+-------+-----------+--------------------+----------+----------+---------+----------+
    |    0|1 BHK Ready to Oc...|Bhiwandi, Thane h...|          42 Lac |             6000|   thane|46.449999999999996|Ready to Move|10 out of 11|     Resale|   Unfurnished|  NULL|                NULL|Srushti Siddhi Ma...|       1|      2|       NULL|                NULL|      NULL|      NULL|     NULL|   50400.0|
    |    1|2 BHK Ready to Oc...|One can find this...|          98 Lac |            13799|   thane|           43.9417|Ready to Move| 3 out of 22|     Resale|Semi-Furnished|  East|         Garden/Park|         Dosti Vihar|       2|   NULL|     1 Open|            Freehold|      NULL|      NULL|     NULL|  117600.0|
    |    2|2 BHK Ready to Oc...|Up for immediate ...|         1.40 Cr |            17500|   thane|           72.3691|Ready to Move|10 out of 29|     Resale|   Unfurnished|  East|         Garden/Park|Sunrise by Kalpataru|       2|   NULL|  1 Covered|            Freehold|      NULL|      NULL|     NULL|  168000.0|
    |    3|1 BHK Ready to Oc...|This beautiful 1 ...|          25 Lac |             NULL|   thane|49.236999999999995|Ready to Move|  1 out of 3|     Resale|   Unfurnished|  NULL|                NULL|                NULL|       1|      1|       NULL|                NULL|      NULL|      NULL|     NULL|   30000.0|
    |    4|2 BHK Ready to Oc...|This lovely 2 BHK...|         1.60 Cr |            18824|   thane|58.991499999999995|Ready to Move|20 out of 42|     Resale|   Unfurnished|  West|Garden/Park, Main...|TenX Habitat Raym...|       2|   NULL|  1 Covered|Co-operative Society|      NULL|      NULL|     NULL|  192000.0|
    +-----+--------------------+--------------------+-----------------+-----------------+--------+------------------+-------------+------------+-----------+--------------+------+--------------------+--------------------+--------+-------+-----------+--------------------+----------+----------+---------+----------+
    only showing top 5 rows
    


## 2. Objetivos de análisis estadístico
### 2.1. Medidas de dispersión (varianza y desviación estándar)


```python
from pyspark.sql.functions import std, variance, avg, max, median


print("Máximo: ")
df.select(max(col("Amount_USD"))).show(truncate=False)
print("Media: ")
df.select(avg(col("Amount_USD"))).show(truncate=False)
print("Mediana: ")
df.select(median(col("Amount_USD"))).show(truncate=False)
print("Varianza: ")
df.select(variance(col("Amount_USD"))).show(truncate=False)
print("Desviación estándar: ")
df.select(std(col("Amount_USD"))).show()
```

    Máximo: 
    +---------------+
    |max(Amount_USD)|
    +---------------+
    |1.6803600384E8 |
    +---------------+
    
    Media: 
    +-----------------+
    |avg(Amount_USD)  |
    +-----------------+
    |143673.9094809754|
    +-----------------+
    
    Mediana: 
    +------------------+
    |median(Amount_USD)|
    +------------------+
    |93600.0           |
    +------------------+
    
    Varianza: 
    +---------------------+
    |var_samp(Amount_USD) |
    +---------------------+
    |2.2369053492349777E11|
    +---------------------+
    
    Desviación estándar: 
    +------------------+
    |   std(Amount_USD)|
    +------------------+
    |472959.33749477635|
    +------------------+
    


La desviación estándar es más o menos tres veces la media. No es una locura, pero sí que es cierto que puede parecer bastante, sobre todo a la escala a la que están los datos. Confiar en el promedio en este caso no sería lo adecuado.

### 2.2. Medidas de Forma (Skewness y Kurtosis)


```python
from pyspark.sql.functions import skewness, kurtosis

print("Asimetría: ")
df.select(skewness(col("Amount_USD"))).show()
print("Coeficiente de curtosis: ")
df.select(kurtosis(col("Amount_USD"))).show()
```

    Asimetría: 
    +--------------------+
    |skewness(Amount_USD)|
    +--------------------+
    |   270.7528623538977|
    +--------------------+
    
    Coeficiente de curtosis: 
    +--------------------+
    |kurtosis(Amount_USD)|
    +--------------------+
    |   91483.85780267783|
    +--------------------+
    


- La curva tiene un valor positivo (de 270, una barbaridad, es probable que haya algún dato mal tomado) por tanto la mayoría de las casas se concentran en los precios bajos y hay pocas casas caras, pero las que hay son muy caras, puede que en el ámbito de millones o puede que cientos de millones (la casa con mayor valor llega casi a los 200 millones de dólares).
- El valor de Curtosis es muy alto, por tanto, hay muchos valores muy concentrados, pero es extremadamente sensible a los valores extremos. Es poco probable que los datos de precio sean erróneos (ciertamente hay casas muy caros), pero sí que es cierto que estos pocos valores están distorsionando los datos. En este caso, sería una buena idea pasar los datos a escala logarítmica.

## 3. Interpretación para IA
### 3.1.- Pre-procesamiento para redes neuronales:


```python
stats = df.select(
    avg("Amount_USD").alias("avg_usd"),
    std("Amount_USD").alias("std_usd")
).collect()[0]

avg_usd = stats["avg_usd"]
std_usd = stats["std_usd"]

stats = df.select(
    avg("Carpet Area").alias("avg_area"),
    std("Carpet Area").alias("std_area")
).collect()[0]

avg_area = stats["avg_area"]
std_area = stats["std_area"]

df_normalized = (
    df
        .withColumn("Amount_USD_Z_Score", (col("Amount_USD") - avg_usd) / std_usd)
        .withColumn("Carpet_Area_Z_Score", (col("Carpet Area") - avg_area) / std_area)
)
df_normalized.select("Amount_USD_Z_Score").show(5)
df_normalized.select("Carpet_Area_Z_Score").show(5)
df_normalized.select(max("Amount_USD_Z_Score")).show()
```

    +--------------------+
    |  Amount_USD_Z_Score|
    +--------------------+
    | -0.1972133798542577|
    |-0.05512928366968411|
    | 0.05143378846874608|
    |-0.24034605191028896|
    | 0.10217810853466522|
    +--------------------+
    only showing top 5 rows
    
    +--------------------+
    | Carpet_Area_Z_Score|
    +--------------------+
    |-0.22972093599364965|
    |-0.23858078173842762|
    |-0.13816919663094365|
    | -0.2198766629438963|
    |-0.18542170726975965|
    +--------------------+
    only showing top 5 rows
    
    +-----------------------+
    |max(Amount_USD_Z_Score)|
    +-----------------------+
    |      354.9825886086313|
    +-----------------------+
    



```python
!pip install pyarrow
```

    Requirement already satisfied: pyarrow in /usr/local/lib/python3.10/site-packages (23.0.1)
    [33mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv[0m[33m
    [0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip is available: [0m[31;49m23.0.1[0m[39;49m -> [0m[32;49m26.0.1[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m


    Comprobación de valores extremos


```python
import matplotlib.pyplot as plt
import seaborn as sns
df_pandas = df.select("Amount_USD").toPandas()
media = df_pandas["Amount_USD"].mean()
mediana = df_pandas["Amount_USD"].median()
print(media, mediana)
print(df_pandas)
plt.figure(figsize=(10, 6))
sns.histplot(df_pandas["Amount_USD"], kde=True, color="skyblue")

# plt.xlim(0, 1.5e10)

# 4. Dibujamos las líneas verticales
# axvline dibuja una línea vertical de arriba a abajo
plt.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Media: {media:.2f}')
plt.axvline(mediana, color='green', linestyle='-', linewidth=2, label=f'Mediana: {mediana:.2f}')

# 5. Ajustes finales
plt.title(f"Distribución de Plazas")
plt.xlabel("Valor")
plt.ylabel("Frecuencia")

# MUY IMPORTANTE: llamar a legend() para que se muestren las etiquetas de media y mediana
plt.legend()

plt.show()
```

    143673.90948097498 93600.0
            Amount_USD
    0        50400.000
    1       117600.000
    2       168000.000
    3        30000.000
    4       192000.000
    ...            ...
    187526   75600.000
    187527   66000.000
    187528   91200.000
    187529   36000.000
    187530  141599.988
    
    [187531 rows x 1 columns]


    /usr/local/lib/python3.10/site-packages/IPython/core/pylabtools.py:170: UserWarning: Creating legend with loc="best" can be slow with large amounts of data.
      fig.canvas.print_figure(bytes_io, **kw)



    
![png](output_17_2.png)
    


### 3.2.- Gestión de outliers (Kurtosis)


```python
quantile_filter = df.approxQuantile("Amount_USD", [0.98], 0.01)[0]
df_limpio = (
    df.filter(col("Amount_USD") < quantile_filter)
)

print("Media: ")
df_limpio.select(avg(col("Amount_USD"))).show(truncate=False)
print("Mediana: ")
df_limpio.select(median(col("Amount_USD"))).show(truncate=False)
print("Varianza: ")
df_limpio.select(variance(col("Amount_USD"))).show(truncate=False)
print("Desviación estándar: ")
df_limpio.select(std(col("Amount_USD"))).show()

print("Asimetría: ")
df_limpio.select(skewness(col("Amount_USD"))).show()
print("Coeficiente de curtosis: ")
df_limpio.select(kurtosis(col("Amount_USD"))).show()
```

    Media: 
    +------------------+
    |avg(Amount_USD)   |
    +------------------+
    |123878.41984043151|
    +------------------+
    
    Mediana: 
    +------------------+
    |median(Amount_USD)|
    +------------------+
    |90000.0           |
    +------------------+
    
    Varianza: 
    +--------------------+
    |var_samp(Amount_USD)|
    +--------------------+
    |9.70796939846777E9  |
    +--------------------+
    
    Desviación estándar: 
    +-----------------+
    |  std(Amount_USD)|
    +-----------------+
    |98529.02820218907|
    +-----------------+
    
    Asimetría: 
    +--------------------+
    |skewness(Amount_USD)|
    +--------------------+
    |  1.5938858958788162|
    +--------------------+
    
    Coeficiente de curtosis: 
    +--------------------+
    |kurtosis(Amount_USD)|
    +--------------------+
    |  2.4296765838913377|
    +--------------------+
    


Al quitar el 1% de los datos más alto el coeficiente de curtosis prácticamente no cambia, pasa de 26000 aprox. a 25000 aprox. (además de bajar la asimetría de 270 a 122). La media aritmética tiene mucha diferencia con la mediana y la desviación estándar está en una escala desproporcionada.   
Sin embargo, si quitasemos el 2% de los valores más altos el coeficiente de kurtosis baja hasta 2.42, lo cuál ya es un valor aceptable. Además la asimetría tiene un valor de 1.59, también más razonable. La desviación estándar ya se encuentra en valores más razonables y la media no está tan diferenciada de la mediana.  
Este cambio confirma la tendencia que se observaba antes muchas casas baratas, y pocas muy caras, con el cambio de que las métricas se encuentran en valores aceptables.
## 4. Análisis de Segmentos (Grouping & Aggregation)
### 4.1.- Ingeniería de variable (Extracción de BHK - Bedroom-Hall-Kitchen)


```python
df = df_limpio
df = (
    df.withColumn("Num_Bedrooms", split(col("Title"), "BHK")[0])
)
df.select("Num_Bedrooms").show(5)
```

    +------------+
    |Num_Bedrooms|
    +------------+
    |          1 |
    |          2 |
    |          2 |
    |          1 |
    |          2 |
    +------------+
    only showing top 5 rows
    


### 4.2.- Cálculo de estadísticas por grupo


```python
from pyspark.sql.functions import cast, count
(
    df
        .groupBy("Num_Bedrooms")
        .agg(
            avg("Amount_USD").alias("Media"),
            median("Amount_USD").alias("Mediana"),
            std("Amount_USD").alias("Desviacion estandar"),
            skewness("Amount_USD").alias("asimetria"),
            count("Amount_USD").alias("cantidad"),
            (std("Amount_USD") / avg("Amount_USD")).alias("Desviacion estandar porcentual"),
            kurtosis("Amount_USD").alias("Kurtosis")

        ).filter(col("Num_Bedrooms").cast("int").isNotNull()).sort("Num_Bedrooms").show(150)
)
```

                                                                                    

    +------------+------------------+--------+-------------------+--------------------+--------+------------------------------+-------------------+
    |Num_Bedrooms|             Media| Mediana|Desviacion estandar|           asimetria|cantidad|Desviacion estandar porcentual|           Kurtosis|
    +------------+------------------+--------+-------------------+--------------------+--------+------------------------------+-------------------+
    |          1 | 42221.53846601398| 30000.0| 31980.109963379917|   3.835382911994782|   10725|            0.7574359231159269| 29.008975883382618|
    |         10 |          265350.0|283800.0| 128209.10375521032|-0.31530187120905473|       8|           0.48316978991976756|-0.5780638767238986|
    |          2 | 72965.82082456016| 63600.0|  44944.85104975612|  2.2458812502778445|   70423|            0.6159712937078037|   9.95950077778739|
    |          3 |154798.93343173715|126000.0|  93801.71454325269|   1.326238712576375|   77612|             0.605958403354356|  1.913981507516274|
    |          4 | 266707.7558344045|270000.0| 119468.97349445987| 0.05666055140478974|   13382|           0.44793963010448284|-0.8893701940999601|
    |          5 |356967.14690489916|438000.0| 119070.83553970927| -0.9636783616665766|     694|           0.33356244845532335|-0.4703250096962326|
    |          6 |253077.55102040817|222000.0| 128390.71108876045| 0.47465368067230734|      49|            0.5073176604210423|-0.7362797869339119|
    |          7 |269538.46153846156|222000.0| 158009.01629580898| 0.43332821947377914|      13|            0.5862206654810264| -1.266064846902077|
    |          8 |          196200.0|196200.0| 246921.68799034238|                 0.0|       2|             1.258520326148534|               -2.0|
    |          9 |          303000.0|294000.0| 125331.56027114639| 0.15506836162301418|       4|            0.4136355124460277|-1.5840887643341242|
    +------------+------------------+--------+-------------------+--------------------+--------+------------------------------+-------------------+
    


## 4.3. Preguntas de análisis para el modelo
### A. Análisis de variabilidad (Desviación Estándar)
- _¿La variabilidad se mantiene constante o se dispara en las propiedades más grandes?_  
  
Al contrario. En las casas de una habitación la desviación estándar llega a ser el 75% de la media o en las de dos, que es el 61% de la media (en tres es igual), mientras que en el resto (con la excepción de las de 8 habitaciones, pero ese número lo vamos a ignorar ya que solo cuenta con dos ejemplos), ronda por el 50% o menos, bajando incluso hasta el 30%.
  
- _Si la desviación es mucho mayor en los pisos de 3BHK que en los de 1BHK, ¿qué nos indica esto sobre la homogeneidad del producto?_  
  
Las casas de 1BHK tienen unos valores muy concentrados, y son muy sensibles a outliers, por eso una desviación estándar porcentual tan alta. En los valores de 2BHK y 3 BHK también hay un coeficiente de curtosis positivo y por ello la desviación estándar también es alta en comparación a la media. En cuanto el coeficiente de curtosis se vuelve negativo la desviación estándar porcentual baja mucho, ya que los registros están mucho más uniformemente distribuidos (con la excepción de 8BHK) y son menos sensibles a outliers.  
Por poner algún ejemplo, si alguien soltero estuviera buscando una casa para él solo de 1BHK, se encontraría muchas casas de precios parecidos con algunas excepciones de precios muy altos. Es probable que se encuentre con muchas viviendas muy similares, mientras que esas que se disparan lo hagan por alguna razón en específico: tener jardín, alguna ubicación privilegiada o ser un edificio muy moderno. Si una pareja con cuatro hijos, buscara una vivienda de 4 BHK, se encontraría con mucha variedad de precios, bastante uniformemente distribuidos. Es muy probable que vieran mucha disparidad en la oferta de vivienda: casas con bastante terreno o nada, ubicaciones muy buenas y muy malas, viviendas modernas y antiguas. Al haber tanta variedad esto afecta a la desviación estándar y la reduce, ya que si hubiera un outlier habría muchos valores que lo "taparían".
### B. Confiabilidad del precio promedio:
- _Basándote en lo anterior, ¿en qué segmento (1BHK o 3BHK) dirías que el "Precio Promedio" es un indicador más fiable del valor real de una propiedad? Es decir, si tuvieras que tasar una propiedad "a ciegas" usando solo el promedio del mercado, ¿en qué tipo de apartamento tendrías más riesgo de equivocarte drásticamente por exceso o por defecto?_  
  
Sería mucho más fiable la predicción en el segmento de 3BHK, por varias razones:
1. Una mayor cantidad de ejemplos
2. Una menor diferencia entre la media y la mediana, lo cuál indica que no hay tantos valores que empujen el promedio hacia un número mayor
3. Una menor desviación estándar porcentual, lo cuál indica que el error promedio va a ser menor en términos relativos
4. Un coeficiente de curtosis en unos valores aceptables. En 1BHK se encuentra casi en 30 lo cuál indica que hay muchos valores muy juntos y mucha cola. En 3BHK también es positivo, sin embargo, mucho menor

### C. Detección de anomalías de mercado (Curtosis):
- _¿Qué segmento tiene una curtosis más alta (colas más pesadas)?_  
  
El segmento con la curtosis más alta es el segmento de 1BHK-3BHK, reduciéndose drásticamente por cada habitación que se añade.  
  
- _¿Si el segmento de 3 BHK tiene una curtosis muy elevada, significa que existen propiedades con precios desorbitados que rempen la norma. ¿Consideras que estas "mansiones" representan la realidad del barrio, o son excepciones que deberían analizarse en un estudio de mercado aparte para no distorsionar la visión general?_  
  
Todas estas excepciones van en un estudio aparte. Esas curtosis (sobre todo la de 1BHK) son síntoma de algunas viviendas que tiene precios desorbitados que no representan la realidad general, por un motivo u otro.
