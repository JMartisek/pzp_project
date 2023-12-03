import threading
import math
import time
import bogosort
from pycuda import driver, compiler, gpuarray, tools
# mam prej 16 threadu
NumberOfThreads = 16



def threadParameters(Data):

    return  math.floor(len(Data) / NumberOfThreads)


def stopWordsCounter(Data):
    threadParameters(Data)

def MFilterSize(data):
    NumberOfItemOnOneThread = threadParameters(data)
    threads = []
    iterator = 0
    lower = []
    middle = []
    higher = []
    result = [lower, middle, higher]
    results = [[],[],[]]
    lck = threading.Lock()

    for i in range(NumberOfThreads):
        Dataset = data[i*NumberOfItemOnOneThread:(1+i)*NumberOfItemOnOneThread]
        t = threading.Thread(target=FilterSize, args=(Dataset,results,i,lck))
        threads.append(t)
        iterator += 1

    start = time.time()
    for i in range(NumberOfThreads):
        threads[i].start()

    for i in range(NumberOfThreads):
        threads[i].join()
    size = len(results)
    for i in range(len(results)):
        for j in results[i]:
            result[i] += j

    stop = time.time()
    print("CPU multithread:", stop - start)
    print("Number of \" middle\" elements:", len(result[1]))
    print("everything is done")

    sortedResult = wordsFrequency(result[1])
    __getTwoItemsFromDict(sortedResult, "size words")
    return result


def bogoPogoPopogo(Dataset,results,i):
    results[i] = bogosort.bogoPogoSort(Dataset)

   # print("thread",i, "is done")

def FilterSize(dataSet, results, i,lck):
    lower = []
    middle = []
    greater = []

    for word in dataSet:
        if len(word) > 7:
            greater.append(word)
        elif len(word) < 5:
            lower.append(word)
        else:
            middle.append(word)
    lck.acquire()
    results[0].append(lower)
    results[1].append(middle)
    results[2].append(greater)
    lck.release()
    #print("thread",i, "is done")

def filterStopWords(data, stopWords):
    NumberOfItemOnOneThread = threadParameters(data)
    threads = []
    results = {}
    lck = threading.Lock()
    for i in range(NumberOfThreads):
        Dataset = data[i*NumberOfItemOnOneThread:(1+i)*NumberOfItemOnOneThread]
        t = threading.Thread(target=filterStopWord, args=(Dataset,stopWords,results,len(Dataset)*i,lck))
        threads.append(t)

    start = time.time()
    for i in range(NumberOfThreads):
        threads[i].start()

    for i in range(NumberOfThreads):
        threads[i].join()
    stop = time.time()
    print("CPU multithread stopWords:", stop - start)
    sortedResult = wordsFrequency(results.values())
    __getTwoItemsFromDict(sortedResult, "stop words")
    return sortedResult

def filterStopWord(data, stopWords, results, AdIndex,lck):
    for index, word in enumerate(data):
        if word in stopWords:
            actualIndex =index+ AdIndex
            lck.acquire()
            results[actualIndex] = word
            lck.release()

def wordsFrequency(data):
    frequencyDic = {}
    for i in data:
        if i in frequencyDic:
            frequencyDic[i] = frequencyDic.get(i) +1
        else:
            frequencyDic[i] = 1
    # bogosort.bogoPogoSort(list(frequencyDic.values()))
    return sorted(frequencyDic.items(), key=lambda x: x[1], reverse=True)

def __getTwoItemsFromDict(dict, type):
    print("First",type," value", dict[0],  "and second", dict[1])