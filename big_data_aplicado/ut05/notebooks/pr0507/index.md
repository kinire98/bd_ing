# PR0507. Creación de un motor de recomendación gastronómico

## Fase 1: Preparación de datos


```python
from pyspark.sql.types import StringType, IntegerType, DoubleType, StructType, StructField, TimestampNTZType, DateType
schema = StructType([
    StructField("user_id", IntegerType(), False),
    StructField("venue", IntegerType(), False),
    StructField("rating", DoubleType(), False),
])
```


```python
from pyspark.sql import SparkSession

spark = (
    SparkSession
        .builder
        .appName("prediccion")
        .master("spark://spark-master:7077")
        .getOrCreate()
)

df = (
    spark
        .read
        .format("csv")
        .schema(schema)
        .option("header", "true")
        .load("/workspace/pr0507/data/ratings.csv")
)


df.show(5)
```

    +-------+-----+------+
    |user_id|venue|rating|
    +-------+-----+------+
    |      1|    1|   5.0|
    |      1|   51|   4.0|
    |      1|   51|   2.0|
    |      1|   51|   5.0|
    |      1|   52|   5.0|
    +-------+-----+------+
    only showing top 5 rows
    



```python
train, test = df.randomSplit([0.8, 0.2], seed=42)
```

## Fase 2: Construcción y búsqueda del modelo óptimo


```python
!pip install numpy
```

    Collecting numpy
      Downloading numpy-2.2.6-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (16.8 MB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m16.8/16.8 MB[0m [31m17.8 MB/s[0m eta [36m0:00:00[0m00:01[0m00:01[0m
    [?25hInstalling collected packages: numpy
    Successfully installed numpy-2.2.6
    [33mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv[0m[33m
    [0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip is available: [0m[31;49m23.0.1[0m[39;49m -> [0m[32;49m26.0.1[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m



```python
from pyspark.ml.recommendation import ALS
print(train.count())
als = ALS(
    maxIter=10,
    regParam=0.1,
    rank=15,
    userCol="user_id",
    itemCol="venue",
    ratingCol="rating",
    coldStartStrategy="drop"
)
model = als.fit(train)
```

    2248543


                                                                                    


```python
from pyspark.ml.evaluation import RegressionEvaluator
evaluator = RegressionEvaluator(
    metricName="rmse",
    labelCol="rating",
    predictionCol="prediction"
)
```


```python
predictions = model.transform(test)
error_rmse = evaluator.evaluate(predictions)
error_rmse
```

                                                                                    




    1.6270567272545742



- regParam = 0.01, rank = 5 -> 3.47
- regParam = 0.01, rank = 10 -> 2.808
- regParam = 0.01, rank = 15 -> 2.536
- regParam = 0.1, rank = 5 -> 1.983
- regParam = 0.1, rank = 10 -> 1.687
- regParam = 0.1, rank = 15 -> 1.62

### CrossValidator


```python
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
als = ALS(
    userCol="user_id",
    itemCol="venue",
    ratingCol="rating",
    coldStartStrategy="drop"
)
grid_params = (
    ParamGridBuilder()
        .addGrid(als.rank, [5, 10, 20])
        .addGrid(als.regParam, [0.01, 0.1, 0.5])
        .addGrid(als.maxIter, [10, 20])
        .build()
)

cross_validator = CrossValidator(
    estimator=als,
    estimatorParamMaps=grid_params,
    evaluator=evaluator,
    numFolds=3
)
optimized_model = cross_validator.fit(df)

```

                                                                                    


```python
optimized_model
```




    CrossValidatorModel_8bd8849b2cc9



## Fase 3: evaluación y resultados


```python

print(f"Best rank: {optimized_model.bestModel.rank}")
print(f"Best regParam: {optimized_model.bestModel._java_obj.parent().getRegParam()}")
```

    Best rank: 20
    Best regParam: 0.5


## Fase 4: Puesta en Producción


```python
from pyspark.sql import functions as F
optimized_model.bestModel.recommendForUserSubset(spark.createDataFrame([(1,)], ["user_id"]), 15).select("user_id", F.explode("recommendations")).show()
```

    [Stage 11025:===============================================>     (72 + 8) / 80]

    +-------+--------------------+
    |user_id|                 col|
    +-------+--------------------+
    |      1|  {679556, 5.494313}|
    |      1|{1129131, 5.4835405}|
    |      1| {970772, 5.4774475}|
    |      1|  {695965, 5.468598}|
    |      1|{1100948, 5.4600663}|
    |      1|   {67411, 5.459571}|
    |      1|  {775560, 5.451147}|
    |      1|  {87569, 5.4484205}|
    |      1| {256026, 5.4441605}|
    |      1|  {769352, 5.433417}|
    |      1|  {598951, 5.428983}|
    |      1|  {322261, 5.427871}|
    |      1| {781721, 5.4269624}|
    |      1|   {27525, 5.426294}|
    |      1|  {912250, 5.424808}|
    +-------+--------------------+
    


                                                                                    
