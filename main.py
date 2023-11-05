import matplotlib.pyplot as plt
import CPU_one_thread
import CPU_multithread
import time
import threading
import bogosort
import psutil


#graphic functions
def pieChart(labels, size):
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.show()




# data load
data = open("data.txt", "r")
data = data.read()
stopData = open("stop_words.txt", "r")
stopData = stopData.read().split()


# cpu one thread version

mujList = CPU_one_thread.parseWords(data)
hashed_data = CPU_one_thread.hash(mujList)
tested_data = CPU_one_thread.testHash(mujList)
start = time.time()
data = CPU_one_thread.filterSize(mujList)
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

freqWrods = CPU_one_thread.wordsFrequency(mujList) #return dict
bogosorted = sorted(list(freqWrods.values()), reverse= True)


print("------------------ CPU ONE THREAD ------------------")
print("Number of stopWords: ", CPU_one_thread.stopWordsCount(stopData, mujList))
print("Filtered by stopwords( index: 'stop word'):", CPU_one_thread.stopWordsFilter(stopData, mujList))
print("There is ", data[0], "words with 4 or less characters")
print("There is ", data[1], "words with 5 - 7 characters")
print("There is ", data[2], "words with 8 or more characters")
print(data[0]+data[1]+data[2], " <- this should be equal to this -> ", len(mujList))
print("It takes ", stop-start, "seconds.")
print("Number of elements in hashed dictionary:", len(hashed_data))
print("Number of elements in normal dictionary:", len(tested_data))
print("Most frequent word is", CPU_one_thread.getValueByKey(freqWrods,bogosorted[0]), "and we have it there", bogosorted[0], "times." )
print("Most used word is \"",CPU_one_thread.getValueByKey(freqWrods, bogosorted[0]), "\"we count ", bogosorted[0])
#pieChart(labels, sizes)

# cpu multithread version
print("")
print("------------------ CPU MULTI THREAD ------------------")

testData2 = [2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8,2,5,4,7,5,6,7,2,5,7,4,65,8,4,6,8]

CPU_multithread.MFilterSize(mujList)


# gpu version


# spark version





input('Press ENTER to exit')