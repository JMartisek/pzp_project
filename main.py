import matplotlib.pyplot as plt
import CPU_one_thread
import time


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
data = CPU_one_thread.filterSize(mujList)
stop = time.time()
labels = ['lower then 5', 'others', 'bigger then 7']
sizes = [data[0], data[1], data[2]]




print("------------------ CPU ONE THREAD ------------------")
print("Number of stopWords: ", CPU_one_thread.stopWordsCount(stopData, mujList))
print("Filtered by stopwords( index: 'stop word'):", CPU_one_thread.stopWordsFilter(stopData, mujList))
print("There is ", data[0], "words with 4 or less characters")
print("There is ", data[1], "words with 5 - 7 characters")
print("There is ", data[2], "words with 8 or more characters")
print(data[0]+data[1]+data[2], " <- this should be equal to this -> ", len(mujList))
print("It takes ", stop-start, "seconds.")
pieChart(labels, sizes)



# cpu multithread version

# gpu version


# spark version





input('Press ENTER to exit')