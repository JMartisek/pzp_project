import matplotlib.pyplot as plt
from CPU_one_thread import OneThreadCPU
import murmurHash
import CPU_multithread
import time
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
Hash_lenght_dict = murmurHash.createHashLenght(parsedData)
Hash_word_dict = murmurHash.createHashWord(parsedData)

hash_stop_dict = murmurHash.createHashWord(stopData)

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

CPU_multithread.MFilterSize(parsedData)

CPU_multithread.filterStopWords(parsedData, stopData,)

class bcolors:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

print( bcolors.OKGREEN +"Warning: No active frommets remain. Continue?" + bcolors.ENDC)

# gpu version


# spark version





input('Press ENTER to exit')