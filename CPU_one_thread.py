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
    lower = 0
    middle = 0
    greater = 0
    for word in dataSet:
        if len(word) > 7:
            greater += 1
        elif len(word) < 5:
            lower += 1
        else:
            middle += 1
    return [lower, middle, greater]

def stopWordsFilter(stopWords, dataSet):
    stopWordsDict = {}
    for index, word in enumerate(dataSet):
        if word in stopWords:
            stopWordsDict[index] = word
    return stopWordsDict