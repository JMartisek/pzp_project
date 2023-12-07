import matplotlib.pyplot as plt
from CPU_one_thread import OneThreadCPU
import murmurHash
import CPU_multithread
import time
import GPU
from Spark import SparkSize, SparkStopWords


def statistic(filteredSizeData, filteredStopWordsData, sizeTime, stopTime):
    print("-----------Filter by size-----------")
    print("The most frequent words found there:")
    print(filteredSizeData[0][0], "is there", filteredSizeData[0][1], "times.")
    print(filteredSizeData[1][0], "is there", filteredSizeData[1][1], "times.")
    print("Filter by size takes", sizeTime, "seconds.")
    print("---------Filter by stopWords---------")
    print("The most frequent words found there:")
    print(filteredStopWordsData[0][0], "is there", filteredStopWordsData[0][1], "times.")
    print(filteredStopWordsData[1][0], "is there", filteredStopWordsData[1][1], "times.")
    print("Filter by size takes", stopTime, "seconds.")
    print("-------------------------------------------")
    print("Process takes", stopTime+sizeTime, "seconds.")

#graphic functions
def pieChart(labels, size):
    fig, ax = plt.subplots()
    ax.pie(size, labels=labels, autopct='%1.1f%%')
    plt.show()


# data load
data = open("data.txt", "r")
data = data.read()
stopData = open("stop_words.txt", "r")
stopData = stopData.read().split()

#parse data
parsedData = OneThreadCPU.parseWords(data)

#hash data
Hash_length_dict = murmurHash.createHashLenght(parsedData)
Hash_word_dict = murmurHash.createHashWord(parsedData)
hashed_data = murmurHash.hashedArray(parsedData)
hash_stop_dict = murmurHash.createHashWord(stopData)
testStopData = ['thee', 'electronic', 'barbarians', 'VERSION', 'summer-house']
testInputData = ['thee', 'electronic', 'barbarians', 'VERSION', 'summer-house']
hashed_testStopData = murmurHash.hashedArray(testStopData)
hashed_StopData = murmurHash.hashedArray(stopData)
hashed_testInputData = murmurHash.hashedArray(testInputData)
hashed_parsedData, parsedDataLenght = murmurHash.hashArray(parsedData)



# cpu one thread version
print("------------------ CPU ONE THREAD ------------------")
cpuVersion1 = OneThreadCPU(False, parsedData, stopData)
cpuSingleThreadData = cpuVersion1.gettAllData()
statistic(cpuSingleThreadData[0],cpuSingleThreadData[2],cpuSingleThreadData[1], cpuSingleThreadData[3]  )

# cpu multi thread version

print("")
print("------------------ CPU MULTI THREAD ------------------")

[CPUSizeWords, CPU_size_interval] =CPU_multithread.MFilterSize(parsedData)

[CPUStopWords, CPU_stop_interval] = CPU_multithread.filterStopWords(parsedData, stopData,)
statistic(CPUSizeWords,CPUStopWords,CPU_size_interval,CPU_stop_interval)
class bcolors:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

print( bcolors.OKGREEN +"Warning: GDE BODY?" + bcolors.ENDC)

# gpu version
print("------------------ GPU MULTI THREAD ------------------")
[filteredSizeData, SizeInterval] = GPU.filterSizeWords(hashed_parsedData, parsedDataLenght, Hash_word_dict, 4, 8)
[filteredStopData, StopInterval] = GPU.filterStopWords(hashed_parsedData, hashed_StopData,Hash_word_dict)
statistic(filteredSizeData, filteredStopData, SizeInterval,StopInterval)
#print("Size:",filteredSizeData, SizeInterval )
#print("Stop:",filteredStopData, StopInterval )
# spark version

print("------------------ SPARK ------------------")
A = [4, 8, 2, 2, 4, 7, 0, 3, 3, 9, 2, 6, 0, 0, 1, 7, 5, 1, 9, 7]
[filteredSparkSizeData, SparkSizeInterval] = SparkSize(parsedData)
[filteredSparkStopData, SparkStopInterval] =SparkStopWords(parsedData,stopData)
statistic(filteredSparkSizeData,filteredSparkStopData,SparkSizeInterval,SparkStopInterval)



input('Press ENTER to exit')