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


# cpu one thread version

cpuVersion1 = OneThreadCPU(True,parsedData)

print("We have ",len(cpuVersion1.middleValue), "filtered words.")



"""
mujList = CPU_one_thread.parseWords(data)
hashed_data = CPU_one_thread.hash(mujList)
tested_data = CPU_one_thread.testHash(mujList)
start = time.time()
data = CPU_one_thread.filterSize(mujList)  # filtered by size
StopWordsFiltered = list(CPU_one_thread.stopWordsFilter(stopData, mujList).values())  # stop words filtered
stop = time.time()
labels = ['lower then 5', 'others', 'bigger then 7']
sizes = [data[0], data[1], data[2]]

testData = {}
testData[22] = 2
testData[88] = 8
testData[66] = 6
testData[11] = 1
testData[33] = 3
testData[44] = 4



freqWrodsStop = CPU_one_thread.wordsFrequency(StopWordsFiltered) #return dict
bogosortedStop = sorted(list(freqWrodsStop.values()), reverse= True)

freqWrodsSize = CPU_one_thread.wordsFrequency(data[1]) #return dict
bogosortedSize = sorted(list(freqWrodsSize.values()), reverse= True)


print("------------------ CPU ONE THREAD ------------------")
print("Number of stopWords: ", CPU_one_thread.stopWordsCount(stopData, mujList))
print("Filtered by stopwords( index: 'stop word'):", CPU_one_thread.stopWordsFilter(stopData, mujList))
print("There is ", data[0], "words with 4 or less characters")
print("There is ", data[1], "words with 5 - 7 characters")
print("There is ", data[2], "words with 8 or more characters")
#print(data[0]+data[1]+data[2], " <- this should be equal to this -> ", len(mujList))  ROZBITE
print("It takes ", stop-start, "seconds.")
print("Number of elements in hashed dictionary:", len(hashed_data))
print("Number of elements in normal dictionary:", len(tested_data))
print("Most frequent word in Size filtered is", CPU_one_thread.getValueByKey(freqWrodsStop,bogosortedStop[0]), "and we have it there", bogosortedStop[0], "times." )
print("Most frequent word in stop words filtered is", CPU_one_thread.getValueByKey(freqWrodsSize,bogosortedSize[0]), "and we have it there", bogosortedSize[0], "times." )
#pieChart(labels, sizes)

# cpu multithread version
print("")
print("------------------ CPU MULTI THREAD ------------------")

testData2 = [2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8]

CPU_multithread.MFilterSize(mujList)

class bcolors:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

print( bcolors.OKGREEN +"Warning: No active frommets remain. Continue?" + bcolors.ENDC)
"""
# gpu version


# spark version





input('Press ENTER to exit')