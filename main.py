import matplotlib.pyplot as plt
from CPU_one_thread import OneThreadCPU
import murmurHash
import CPU_multithread
import GPU
from Spark import SparkSize, SparkStopWords


def statistic(SizeData, StopWordsData, sizeTime, stopTime):
    print("-----------Filter by size-----------")
    print("The most frequent words found there:")
    print(SizeData[0][0], "is there", SizeData[0][1], "times.")
    print(SizeData[1][0], "is there", SizeData[1][1], "times.")
    print("Filter by size takes", sizeTime, "seconds.")
    print("---------Filter by stopWords---------")
    print("The most frequent words found there:")
    print(StopWordsData[0][0], "is there", StopWordsData[0][1], "times.")
    print(StopWordsData[1][0], "is there", StopWordsData[1][1], "times.")
    print("Filter by size takes", stopTime, "seconds.")
    print("-------------------------------------------")
    print("Process takes", stopTime+sizeTime, "seconds.")


# graphic function
def pieChart(labels, size, title, index):
    #plt.figure(index)
    fig, axs = plt.subplots(1,2+index)
    for i in range(2+index):
        axs[i].pie(size[i], labels=labels, autopct='%1.1f%%')
        axs[i].set_title(title[i])
    if(index == 1):
        plt.show(block=False)
    else:
        plt.show()



# data load
data = open("data.txt", "r")
data = data.read()
stopData = open("stop_words.txt", "r")
stopData = stopData.read().split()

# parse data
parsedData = OneThreadCPU.parseWords(data)

# hash data
Hash_length_dict = murmurHash.createHashLenght(parsedData)
Hash_word_dict = murmurHash.createHashWord(parsedData)
hashed_data = murmurHash.hashedArray(parsedData)
hash_stop_dict = murmurHash.createHashWord(stopData)
hashed_StopData = murmurHash.hashedArray(stopData)
[hashed_parsedData, parsedDataLenght] = murmurHash.hashArray(parsedData)


print("-------------------- CPU ONE THREAD --------------------")
cpuVersion1 = OneThreadCPU(parsedData, stopData)
cpuSingleThreadData = cpuVersion1.gettAllData()
statistic(cpuSingleThreadData[0], cpuSingleThreadData[2], cpuSingleThreadData[1], cpuSingleThreadData[3])


print("")
print("------------------- CPU MULTI THREAD -------------------")
[CPUSizeWords, CPU_size_interval] = CPU_multithread.MFilterSize(parsedData)
[CPUStopWords, CPU_stop_interval] = CPU_multithread.filterStopWords(parsedData, stopData,)
statistic(CPUSizeWords, CPUStopWords, CPU_size_interval, CPU_stop_interval)


print("------------------- GPU MULTI THREAD -------------------")
[filteredSizeData, SizeInterval] = GPU.filterSizeWords(hashed_parsedData, parsedDataLenght, Hash_word_dict, 4, 8)
[filteredStopData, StopInterval] = GPU.filterStopWords(hashed_parsedData, hashed_StopData, Hash_word_dict)
statistic(filteredSizeData, filteredStopData, SizeInterval, StopInterval)


print("------------------------ SPARK -------------------------")
[filteredSparkSizeData, SparkSizeInterval] = SparkSize(parsedData)
[filteredSparkStopData, SparkStopInterval] = SparkStopWords(parsedData, stopData)
statistic(filteredSparkSizeData, filteredSparkStopData, SparkSizeInterval, SparkStopInterval)



pieChart(["CPU single thread", "CPU multithread", "GPU", "Spark"],
         [[cpuSingleThreadData[1]+cpuSingleThreadData[3],CPU_size_interval+CPU_stop_interval,
           SizeInterval+StopInterval, SparkSizeInterval + SparkStopInterval],[cpuSingleThreadData[1],CPU_size_interval,
        SizeInterval, SparkSizeInterval],[cpuSingleThreadData[3],CPU_stop_interval,StopInterval, SparkStopInterval]],
         ["Filter size and stop word","Filter size","Filter stop word"], 1)

pieChart(["Filter size", "Filter stopWords"], [[cpuSingleThreadData[1],cpuSingleThreadData[3]],[CPU_size_interval,CPU_stop_interval],[SizeInterval,StopInterval],[SparkSizeInterval,SparkStopInterval]],["CPU single thread", "CPU multithread","GPU", "Spark"],2)



input('Press ENTER to exit')
