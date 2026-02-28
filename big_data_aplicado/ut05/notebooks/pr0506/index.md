# PR0506. Análisis de comportamiento de usuarios en Netflix
## Definición de esquema y comienzo de sesión Spark


```python
from pyspark.sql.types import StringType, IntegerType, DoubleType, StructType, StructField, TimestampNTZType, DateType
schema = StructType([
    StructField("", IntegerType(), False),
    StructField("datetime", TimestampNTZType(), False),
    StructField("duration", DoubleType(), False),
    StructField("title", StringType(), False),
    StructField("genres", StringType(), False),
    StructField("release_date", DateType(), False), 
    StructField("movie_id", StringType(), False),
    StructField("user_id", StringType(), False),
])
```


```python
from pyspark.sql import SparkSession

spark = (
    SparkSession
        .builder
        .appName("Netflix")
        .master("spark://spark-master:7077")
        .getOrCreate()
)

df = (
    spark
        .read
        .format("csv")
        .schema(schema)
        .option("header", "true")
        .load("/workspace/pr0506/vodclickstream_uk_movies_03.csv")
)


df.show(5)
```

    +-----+-------------------+--------+--------------------+--------------------+------------+----------+----------+
    |     |           datetime|duration|               title|              genres|release_date|  movie_id|   user_id|
    +-----+-------------------+--------+--------------------+--------------------+------------+----------+----------+
    |58773|2017-01-01 01:15:09|     0.0|Angus, Thongs and...|Comedy, Drama, Ro...|  2008-07-25|26bd5987e8|1dea19f6fe|
    |58774|2017-01-01 13:56:02|     0.0|The Curse of Slee...|Fantasy, Horror, ...|  2016-06-02|f26ed2675e|544dcbc510|
    |58775|2017-01-01 15:17:47| 10530.0|   London Has Fallen|    Action, Thriller|  2016-03-04|f77e500e7a|7cbcc791bf|
    |58776|2017-01-01 16:04:13|    49.0|            Vendetta|       Action, Drama|  2015-06-12|c74aec7673|ebf43c36b6|
    |58777|2017-01-01 19:16:37|     0.0|The SpongeBob Squ...|Animation, Action...|  2004-11-19|a80d6fc2aa|a57c992287|
    +-----+-------------------+--------+--------------------+--------------------+------------+----------+----------+
    only showing top 5 rows
    


## Ejercicios
### 1.- Auditoría de telemetría Web (validación de datos)


```python
from pyspark.sql import Window, functions as F

user_window = ( Window
                    .partitionBy("user_id")
                    .orderBy("datetime")
)


df = (
    df
        .withColumn("calculated_time_to_next", F.lead(F.unix_timestamp("datetime"), 1).over(user_window) - F.unix_timestamp(F.col("datetime")))
)

df.show(15)
```

    +------+-------------------+--------+--------------------+--------------------+------------+----------+----------+-----------------------+
    |      |           datetime|duration|               title|              genres|release_date|  movie_id|   user_id|calculated_time_to_next|
    +------+-------------------+--------+--------------------+--------------------+------------+----------+----------+-----------------------+
    |139643|2017-05-19 20:21:43|     0.0|                XOXO|        Drama, Music|  2016-08-26|7369676dec|0006ea6b5c|                  91971|
    |140442|2017-05-20 21:54:34|     0.0|            Hot Fuzz|Action, Comedy, M...|  2007-04-20|6467fee6b6|0006ea6b5c|                 506607|
    |144717|2017-05-26 18:38:01|     0.0|         War Machine|  Comedy, Drama, War|  2017-05-26|0f3b137f4e|0006ea6b5c|                  17625|
    |144301|2017-05-26 23:31:46|     0.0|          Apocalypto|Action, Adventure...|  2006-12-08|40dd7bf1f9|0006ea6b5c|                  83635|
    |145323|2017-05-27 22:45:41|     0.0|Joshua: Teenager ...|         Documentary|  2017-01-20|4a138aeefc|0006ea6b5c|                 518737|
    |150621|2017-06-02 22:51:18|  1182.0|         Lucid Dream|    Sci-Fi, Thriller|  2017-06-02|27b44a3183|0006ea6b5c|                   1182|
    |150043|2017-06-02 23:11:00|     0.0|Stranger than Fic...|Comedy, Drama, Fa...|  2006-11-10|73183024a6|0006ea6b5c|                  81826|
    |151464|2017-06-03 21:54:46|  4200.0|Handsome: A Netfl...|     Comedy, Mystery|  2017-05-05|9f2550ca52|0006ea6b5c|                   4200|
    |150783|2017-06-03 23:04:46|     0.0|        Dragon Blade|Action, Adventure...|  2015-09-04|ed515d444e|0006ea6b5c|                  87798|
    |151782|2017-06-04 23:28:04|  1800.0|        Dragon Blade|Action, Adventure...|  2015-09-04|ed515d444e|0006ea6b5c|                 424015|
    |156021|2017-06-09 21:14:59|     0.0|        Shimmer Lake|Crime, Drama, Mys...|  2017-06-09|09a559f1ce|0006ea6b5c|                  94226|
    |156307|2017-06-10 23:25:25|  4800.0| Absolutely Anything|      Comedy, Sci-Fi|  2017-05-12|1e7ac0d4d4|0006ea6b5c|                 618404|
    |162033|2017-06-18 03:12:09|     0.0|     A Plastic Ocean|         Documentary|  2017-04-19|9ac5a606e0|0006ea6b5c|                 153005|
    |162421|2017-06-19 21:42:14|  4831.0|    Bulletproof Monk|Action, Comedy, F...|  2003-04-16|42689f3587|0006ea6b5c|                 786194|
    |170114|2017-06-29 00:05:28|     0.0|                Okja|Action, Adventure...|  2017-06-28|0b1cdb1a41|0006ea6b5c|                   NULL|
    +------+-------------------+--------+--------------------+--------------------+------------+----------+----------+-----------------------+
    only showing top 15 rows
    


Hay muchas discrepancias, porque si un usuario cierra la ventana no cuenta cómo duración, mientras que nuestro cálculo sí que lo tiene en cuenta. Sin embargo, hay otros en los que este valor se acerca mucho más al otro.  
### 2.- Detección de “zapping”


```python

df = (
    df
        .withColumn("is_zapping", F.when((F.col("duration") < 300) | (F.col("duration") == 0), 1).otherwise(0))
)
df.show(15)
```

    +------+-------------------+--------+--------------------+--------------------+------------+----------+----------+-----------------------+----------+
    |      |           datetime|duration|               title|              genres|release_date|  movie_id|   user_id|calculated_time_to_next|is_zapping|
    +------+-------------------+--------+--------------------+--------------------+------------+----------+----------+-----------------------+----------+
    |139643|2017-05-19 20:21:43|     0.0|                XOXO|        Drama, Music|  2016-08-26|7369676dec|0006ea6b5c|                  91971|         1|
    |140442|2017-05-20 21:54:34|     0.0|            Hot Fuzz|Action, Comedy, M...|  2007-04-20|6467fee6b6|0006ea6b5c|                 506607|         1|
    |144717|2017-05-26 18:38:01|     0.0|         War Machine|  Comedy, Drama, War|  2017-05-26|0f3b137f4e|0006ea6b5c|                  17625|         1|
    |144301|2017-05-26 23:31:46|     0.0|          Apocalypto|Action, Adventure...|  2006-12-08|40dd7bf1f9|0006ea6b5c|                  83635|         1|
    |145323|2017-05-27 22:45:41|     0.0|Joshua: Teenager ...|         Documentary|  2017-01-20|4a138aeefc|0006ea6b5c|                 518737|         1|
    |150621|2017-06-02 22:51:18|  1182.0|         Lucid Dream|    Sci-Fi, Thriller|  2017-06-02|27b44a3183|0006ea6b5c|                   1182|         0|
    |150043|2017-06-02 23:11:00|     0.0|Stranger than Fic...|Comedy, Drama, Fa...|  2006-11-10|73183024a6|0006ea6b5c|                  81826|         1|
    |151464|2017-06-03 21:54:46|  4200.0|Handsome: A Netfl...|     Comedy, Mystery|  2017-05-05|9f2550ca52|0006ea6b5c|                   4200|         0|
    |150783|2017-06-03 23:04:46|     0.0|        Dragon Blade|Action, Adventure...|  2015-09-04|ed515d444e|0006ea6b5c|                  87798|         1|
    |151782|2017-06-04 23:28:04|  1800.0|        Dragon Blade|Action, Adventure...|  2015-09-04|ed515d444e|0006ea6b5c|                 424015|         0|
    |156021|2017-06-09 21:14:59|     0.0|        Shimmer Lake|Crime, Drama, Mys...|  2017-06-09|09a559f1ce|0006ea6b5c|                  94226|         1|
    |156307|2017-06-10 23:25:25|  4800.0| Absolutely Anything|      Comedy, Sci-Fi|  2017-05-12|1e7ac0d4d4|0006ea6b5c|                 618404|         0|
    |162033|2017-06-18 03:12:09|     0.0|     A Plastic Ocean|         Documentary|  2017-04-19|9ac5a606e0|0006ea6b5c|                 153005|         1|
    |162421|2017-06-19 21:42:14|  4831.0|    Bulletproof Monk|Action, Comedy, F...|  2003-04-16|42689f3587|0006ea6b5c|                 786194|         0|
    |170114|2017-06-29 00:05:28|     0.0|                Okja|Action, Adventure...|  2017-06-28|0b1cdb1a41|0006ea6b5c|                   NULL|         1|
    +------+-------------------+--------+--------------------+--------------------+------------+----------+----------+-----------------------+----------+
    only showing top 15 rows
    



### 3.- El ranking de "maratones"  


```python
df = (
    df
        .withColumn("date", F.to_date(F.col("datetime")))
)

window = (
    Window
        .partitionBy("user_id", "date")
        .orderBy("datetime")
)


df.withColumn("row_counter", F.row_number().over(window)).filter(F.col("row_counter") > 5).select("user_id", "date").distinct().show(15)
```

    +----------+----------+
    |   user_id|      date|
    +----------+----------+
    |00b88bd923|2017-10-23|
    |0141ae3d9a|2019-02-20|
    |015d339273|2019-01-20|
    |020c9c652a|2019-01-20|
    |023d43562c|2017-05-28|
    |0244e5d9eb|2017-08-22|
    |02751be82b|2017-07-22|
    |02a445c1b1|2017-06-12|
    |02bbf94ed5|2017-04-08|
    |02c54679dd|2018-04-06|
    |02cd2456b2|2018-03-30|
    |032898773f|2018-02-16|
    |036344729a|2017-02-26|
    |03da9f71f4|2017-04-20|
    |04c6fce5ff|2018-11-19|
    +----------+----------+
    only showing top 15 rows
    


### 4.- Análisis de re-visualización


```python
window = (
    Window
        .partitionBy("user_id", "movie_id")
        .orderBy("datetime")
)

df.filter(F.col("datetime").between("2017-01-01", "2019-12-31")).withColumn("counter", F.row_number().over(window)).filter(F.col("counter") > 3).select("user_id", "movie_id").distinct().show(15)
```

    +----------+----------+
    |   user_id|  movie_id|
    +----------+----------+
    |000296842d|e847f14da5|
    |00305e5c73|ea4d08cf70|
    |004e33f215|c590147027|
    |005f639f10|1fd2f8a29f|
    |00691f60a9|3db668b28a|
    |00870a4069|8f2dc77522|
    |00945e0131|5837d75330|
    |014db9dde6|59e398c3e4|
    |0192bd515e|69934edb9a|
    |01b5b53f6b|841aed99d7|
    |01ee5110ec|a97868a9f6|
    |01fedd0701|4fe1783350|
    |023d43562c|13a4ff3605|
    |02b27a6af9|a215824200|
    |02bac90f90|5b27e079e9|
    +----------+----------+
    only showing top 15 rows
    

