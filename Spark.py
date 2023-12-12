import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length, expr
from GPU import __wordsFrequency, __getTwoItemsFromDict


# 12 cores
def SparkSize(data):
    spark = SparkSession.builder.appName("example").config("spark.cores.max", "12").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    df = spark.createDataFrame([(word,) for word in data], ["word"])
    start = time.time()
    filtered_df = df.filter((length(col("word")) > 4) & (length(col("word")) < 8))

    filtered_words_list = [row["word"] for row in filtered_df.collect()]
    stop = time.time()
    return [__getTwoItemsFromDict(__wordsFrequency(filtered_words_list)), stop - start]


def SparkStopWords(data, stopWords):
    spark = SparkSession.builder.appName("example").config("spark.cores.max", "12").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    df = spark.createDataFrame([(idx, value) for idx, value in enumerate(data)], ["index", "value"])
    start = time.time()

    filtered_df = df.filter(expr("value IN ({})".format(",".join("'{}'".format(v) for v in stopWords))))
    # StopWordsWithIndex = [(row["value"], row["index"]) for row in filtered_df.collect()]
    found_words = [row["value"] for row in filtered_df.collect()]

    stop = time.time()

    return [__getTwoItemsFromDict(__wordsFrequency(found_words)), stop - start]