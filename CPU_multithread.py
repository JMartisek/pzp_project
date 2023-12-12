import threading
import math
import time
import bogosort
from GPU import __getTwoItemsFromDict

NumberOfThreads = 16


def threadParameters(Data):
    return  math.floor(len(Data) / NumberOfThreads)


def MFilterSize(data):
    NumberOfItemOnOneThread = threadParameters(data)
    threads = []
    iterator = 0
    lower = []
    middle = []
    higher = []
    result = [lower, middle, higher]
    results = [[], [], []]
    lck = threading.Lock()

    for i in range(NumberOfThreads):
        Dataset = data[i*NumberOfItemOnOneThread:(1+i)*NumberOfItemOnOneThread]
        t = threading.Thread(target=FilterSize, args=(Dataset, results, i, lck))
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

    sortedResult = wordsFrequency(result[1])

    return [__getTwoItemsFromDict(sortedResult), stop - start]


def bogoPogoPopogo(Dataset,results,i):
    results[i] = bogosort.bogoPogoSort(Dataset)


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
    sortedResult = wordsFrequency(results.values())

    return [__getTwoItemsFromDict(sortedResult), stop - start]


def filterStopWord(data, stopWords, results, AdIndex,lck):
    for index, word in enumerate(data):
        if word in stopWords:
            actualIndex = index + AdIndex
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
    return sorted(frequencyDic.items(), key=lambda x: x[1], reverse=True)
