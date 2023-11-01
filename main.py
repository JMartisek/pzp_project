import matplotlib.pyplot as plt
import CPU_one_thread
import time
import threading
import bogosort


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
start = time.time()
mujList = CPU_one_thread.parseWords(data)
hashed_data = CPU_one_thread.hash(mujList)
tested_data = CPU_one_thread.testHash(mujList)
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
bogosorted = bogosort.bogoPogoSort(list(testData.values()))


print(bogosorted)
print(list(testData.keys())[list(testData.values()).index(bogosorted[0])])
print(CPU_one_thread.getValueByKey(testData, bogosorted[0]))




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
pieChart(labels, sizes)



# cpu multithread version

# gpu version


# spark version





input('Press ENTER to exit')