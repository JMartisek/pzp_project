import matplotlib.pyplot as plt
from CPU_one_thread import OneThreadCPU
import murmurHash
import CPU_multithread
import time
import GPU
import threading
import bogosort
import psutil


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
hashed_StopData = murmurHash.hashedArray(stopData)

hashed_parsedData, parsedDataLenght = murmurHash.hashArray(parsedData)

# cpu one thread version
print("------------------ CPU ONE THREAD ------------------")
start = time.time()
cpuVersion1 = OneThreadCPU(False, parsedData, stopData)
stop = time.time()

print("CPU single thread without hash take ", stop-start, "seconds")

# cpu multi thread version

print("")
print("------------------ CPU MULTI THREAD ------------------")

testData2 = [2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8]
testData3 = [1, 2, 3]
CPU_multithread.MFilterSize(parsedData)

CPU_multithread.filterStopWords(parsedData, stopData,)

class bcolors:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

print( bcolors.OKGREEN +"Warning: No active frommets remain. Continue?" + bcolors.ENDC)

# gpu version
print("------------------ GPU MULTI THREAD ------------------")
GPU.filterSizeWords(hashed_parsedData,parsedDataLenght,Hash_word_dict, 4,8)

# pokus o rozdeleni dat pro moznost spusteni stop_word filtru
part1 = hashed_parsedData[0:len(hashed_data)//2]
part2 = hashed_parsedData[len(hashed_data)//2:]
print("part one have", len(part1), "items and part two have", len(part2), "items")

GPU.filterStopWords(hashed_parsedData, hashed_StopData) #test
# spark version





input('Press ENTER to exit')