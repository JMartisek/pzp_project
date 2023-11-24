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
    DataSets = []
    Dataset = []
    threads = []
    iterator = 0
    results = [0,0,0]
    for i in range(NumberOfThreads):
        Dataset = data[i*NumberOfItemOnOneThread:(1+i)*NumberOfItemOnOneThread]
        t = threading.Thread(target=FilterSize, args=(Dataset,results,i,))
        threads.append(t)
        iterator += 1

    start = time.time()
    for i in range(NumberOfThreads):
        threads[i].start()

    for i in range(NumberOfThreads):
        threads[i].join()

    stop = time.time()
    print("multi:", stop - start)
    print(results)
    print("everything is done")


def bogoPogoPopogo(Dataset,results,i):
    results[i] = bogosort.bogoPogoSort(Dataset)

   # print("thread",i, "is done")

def FilterSize(dataSet, results, i):
    lower = 0
    middle = 0
    greater = 0
    lck = threading.Lock()
    for word in dataSet:
        if len(word) > 7:
            greater += 1
        elif len(word) < 5:
            lower += 1
        else:
            middle += 1
    lck.acquire()
    results[0] += lower
    results[1] += middle
    results[2] += greater
    lck.release()
    #print("thread",i, "is done")



