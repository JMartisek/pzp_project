import murmurHash
import bogosort

def parseWords(array):
    return cleanWords(array.split())

def checkLen(word):
    if(len(word) == 0):
        return False
    return True
def weirdStringParser(list, word, index):
    partioned = word.partition("--")
    list[index] = partioned[0]
    list.insert(index+1,partioned[2])
    return list

def stopWordsCount(stopWords, data):
    counter = 0
    for i in data:
        if i in stopWords:
            counter +=1
    return counter

def cleanWords(array):
    repeat = True
    susWords = []
    lastWordList = [",", ")", ".", "\"", "-", ":", ";", "!", "?"]
    firstWordList = ["\"", "-", "("]
    for index, a in enumerate(array):
        repeat = True

        while (repeat == True):
            repeat = False
            if checkLen(a) > 0:
                if a[
                    len(a) - 1] in lastWordList:  # == "," or a[0] == ")" or a[len(a) - 1] == "." or a[len(a) - 1] == "\"" or a[len(a) - 1] == "-" or a[len(a) - 1] == ":" or a[len(a) - 1] == ";" or a[len(a) - 1] == "!"or a[len(a) - 1] == "?":
                    a = a[0:len(a) - 1]
                    array[index] = a
                    repeat = checkLen(a)

                elif a[0] in firstWordList:  # == "\"" or a[0] == "-" or a[0] == "(":
                    a = a[1:]
                    array[index] = a
                    repeat = checkLen(a)
                if "--" in a:
                    array = weirdStringParser(array, a, index)
    return array

def filterSize(dataSet):
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
    return [lower, middle, greater]

def stopWordsFilter(stopWords, dataSet):
    stopWordsDict = {}
    for index, word in enumerate(dataSet):
        if word in stopWords:
            stopWordsDict[index] = word
    return stopWordsDict


def hash(data):
    MyTextDictionary = {}
    for i in data:
        MyTextDictionary[murmurHash.murmur64(i)] = len(i)
    return MyTextDictionary

def singleHash(word):
    return murmurHash.murmur64(word)

def testHash(data):
    myTestDictionary = {}
    for i in data:
        myTestDictionary[i] = len(i)
    return myTestDictionary

def wordsFrequency(data):
    frequencyDic = {}
    for i in data:
        if i in frequencyDic:
            frequencyDic[i] = frequencyDic.get(i) +1
        else:
            frequencyDic[i] = 1
    #bogosort.bogoPogoSort(list(frequencyDic.values()))
    #frequencyDic = sorted(list(frequencyDic.values()), reverse=True)
    return frequencyDic

def getValueByKey(data, key):
    val = list(data.keys())[list(data.values()).index(key)]
    return val






