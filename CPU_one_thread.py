import murmurHash
import bogosort




class OneThreadCPU:
    lessThen4 = []
    middleValue = []
    greaterThen8 = []
    stopWords = []
    MostFrequentWord = []
    __privateVariable = 0


    def __init__(self, hashed, data ):
        print("CPU one thread is starting ...")
        if hashed == True:
            OneThreadCPU.__filterSizeWord(data)
        else:
            print("Not ready yet..")
        # vsechny vystupy jako instance classy, tedy: 3 pole a v kazdem rozdeleni do delky slov

    @staticmethod
    def parseWords(array):
        return OneThreadCPU.__cleanWords(array.split())

    def __checkLen(word):
        if(len(word) == 0):
            return False
        return True
    def __weirdStringParser(list, word, index):
        partioned = word.partition("--")
        list[index] = partioned[0]
        list.insert(index+1,partioned[2])
        return list

    def __stopWordsCount(stopWords, data):
        counter = 0
        for i in data:
            if i in stopWords:
                counter +=1
        return counter

    def __cleanWords(array):
        repeat = True
        susWords = []
        lastWordList = [",", ")", ".", "\"", "-", ":", ";", "!", "?"]
        firstWordList = ["\"", "-", "("]
        for index, a in enumerate(array):
            repeat = True

            while (repeat == True):
                repeat = False
                if OneThreadCPU.__checkLen(a) > 0:
                    if a[
                        len(a) - 1] in lastWordList:  # == "," or a[0] == ")" or a[len(a) - 1] == "." or a[len(a) - 1] == "\"" or a[len(a) - 1] == "-" or a[len(a) - 1] == ":" or a[len(a) - 1] == ";" or a[len(a) - 1] == "!"or a[len(a) - 1] == "?":
                        a = a[0:len(a) - 1]
                        array[index] = a
                        repeat = OneThreadCPU.__checkLen(a)

                    elif a[0] in firstWordList:  # == "\"" or a[0] == "-" or a[0] == "(":
                        a = a[1:]
                        array[index] = a
                        repeat = OneThreadCPU.__checkLen(a)
                    if "--" in a:
                        array = OneThreadCPU.__weirdStringParser(array, a, index)
        return array

    def __filterSizeWord(dataSet):
        for word in dataSet:
            if len(word) > 7:
                OneThreadCPU.greaterThen8.append(word)
            elif len(word) < 5:
                OneThreadCPU.lessThen4.append(word)
            else:
                OneThreadCPU.middleValue.append(word)

    def __stopWordsFilter(stopWords, dataSet):
        stopWordsDict = {}
        for index, word in enumerate(dataSet):
            if word in stopWords:
                stopWordsDict[index] = word
        return stopWordsDict


    def __wordsFrequency(data):
        frequencyDic = {}
        for i in data:
            if i in frequencyDic:
                frequencyDic[i] = frequencyDic.get(i) +1
            else:
                frequencyDic[i] = 1
        #bogosort.bogoPogoSort(list(frequencyDic.values()))
        #frequencyDic = sorted(list(frequencyDic.values()), reverse=True)
        return frequencyDic

    def __getValueByKey(data, key):
        val = list(data.keys())[list(data.values()).index(key)]
        return val







