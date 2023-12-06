import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length, expr


# 12 cores
def SparkSize(data):
    spark = SparkSession.builder.appName("example").getOrCreate()

    # Příklad DataFrame
    columns = ["word"]
    df = spark.createDataFrame([(word,) for word in data], ["word"])
    start = time.time()
    # Použití funkce length k filtrování délky slova
    filtered_df = df.filter((length(col("word")) > 4) & (length(col("word")) < 8))

    # Převod DataFrame na Python list
    filtered_words_list = filtered_df.select("word").rdd.flatMap(lambda x: x).collect()
    stop = time.time()
    print("Spark filter size takes", stop - start, "seconds")
    # Zobrazení výsledného DataFrame
    filtered_df.show()
    #print(data)
def SparkStopWords(big_array,small_array):
    spark = SparkSession.builder.appName("example").getOrCreate()
    df = spark.createDataFrame([(idx, value) for idx, value in enumerate(big_array)], ["index", "value"])
    start = time.time()
    # Filtrování podle hodnot ze smaller_array a vybírání indexů
    filtered_df = df.filter(expr("value IN ({})".format(",".join("'{}'".format(v) for v in small_array))))
    stop = time.time()
    print("Spark filter stop words takes", stop - start, "seconds")
    # Zobrazení výsledného DataFrame
    filtered_df.show()