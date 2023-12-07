import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length, expr
from GPU import __wordsFrequency, __getTwoItemsFromDict


# 12 cores
def SparkSize(data):

    spark = SparkSession.builder.appName("example").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    # Příklad DataFrame
    columns = ["word"]
    df = spark.createDataFrame([(word,) for word in data], ["word"])
    start = time.time()
    # Použití funkce length k filtrování délky slova
    filtered_df = df.filter((length(col("word")) > 4) & (length(col("word")) < 8))

    # Převod DataFrame na Python list
    filtered_words_list = [row["word"] for row in filtered_df.collect()]
    stop = time.time()
    print("Spark filter size takes", stop - start, "seconds")
    # Zobrazení výsledného DataFrame
    #filtered_df.show()
    #print(data)
    return [__getTwoItemsFromDict(__wordsFrequency(filtered_words_list)), stop - start]


def SparkStopWords(big_array, small_array):
    spark = SparkSession.builder.appName("example").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    df = spark.createDataFrame([(idx, value) for idx, value in enumerate(big_array)], ["index", "value"])
    start = time.time()

    # Filtering based on values from smaller_array and selecting indices
    filtered_df = df.filter(expr("value IN ({})".format(",".join("'{}'".format(v) for v in small_array))))

    # Collecting the results as a list of tuples
    result_tuples = [(row["value"], row["index"]) for row in filtered_df.collect()]

    # Extracting the list of found words
    found_words = [row["value"] for row in filtered_df.collect()]

    stop = time.time()

    return [__getTwoItemsFromDict(__wordsFrequency(found_words)), stop - start]