import time


class OneThreadCPU:
    data = []
    lessThen4 = []
    middleValue = []
    greaterThen8 = []
    stopWords = []
    MostFrequentWord = []
    indexStopWordsDict = {}
    countStopWordDict = {}
    countSizeWordDict = {}
    sizeTime = 0
    stopTime = 0

    __privateVariable = 0

    def __init__(self, data, stopWords):
        self.data = data
        self.stopWords = stopWords
        OneThreadCPU.__filterSizeWord(self)
        self.countSizeWordDict = OneThreadCPU.__wordsFrequency( self.middleValue)
        OneThreadCPU.__getTwoItemsFromDict(self,self.countSizeWordDict, "filter size")
        OneThreadCPU.__stopWordsFilter(self)
        self.countStopWordDict = OneThreadCPU.__wordsFrequency( self.indexStopWordsDict.values())
        OneThreadCPU.__getTwoItemsFromDict(self,self.countStopWordDict, "stop word")

    def gettAllData(self):
        SizeArray = []
        for i in self.countSizeWordDict:
            SizeArray.append(i[0])
        return [self.SizeTwo,self.sizeTime, self.StopWordTwo,self.stopTime]

    @staticmethod
    def parseWords(array):
        return OneThreadCPU.__cleanWords(array.split())

    @staticmethod
    def __checkLen(word):
        if(len(word) == 0):
            return False
        return True

    @staticmethod
    def __weirdStringParser(output, word, index):
        partioned = word.partition("--")
        output[index] = partioned[0]
        output.insert(index+1,partioned[2])
        return output

    @staticmethod
    def __cleanWords(array):
        repeat = True
        lastWordList = [",", ")", ".", "\"", "-", ":", ";", "!", "?"]
        firstWordList = ["\"", "-", "(", "ï", "»", "¿"]
        for index, a in enumerate(array):
            repeat = True

            while repeat == True:
                repeat = False
                if OneThreadCPU.__checkLen(a) > 0:
                    if a[len(a) - 1] in lastWordList:
                        a = a[0:len(a) - 1]
                        array[index] = a
                        repeat = OneThreadCPU.__checkLen(a)

                    elif a[0] in firstWordList:
                        a = a[1:]
                        array[index] = a
                        repeat = OneThreadCPU.__checkLen(a)
                    if "--" in a:
                        array = OneThreadCPU.__weirdStringParser(array, a, index)
        return array

    @staticmethod
    def __filterSizeWord(self):
        start = time.time()
        for word in self.data:
            if len(word) > 7:
                OneThreadCPU.greaterThen8.append(word)
            elif len(word) < 5:
                OneThreadCPU.lessThen4.append(word)
            else:
                OneThreadCPU.middleValue.append(word)
        stop = time.time()
        self.sizeTime = stop - start

    @staticmethod
    def __stopWordsFilter(self):
        start = time.time()
        for index, word in enumerate(self.data):
            if word in self.stopWords:
                self.indexStopWordsDict[index] = word
        stop = time.time()
        self.stopTime = stop - start

    @staticmethod
    def __wordsFrequency(data):
        frequencyDic = {}
        for i in data:
            if i in frequencyDic:
                frequencyDic[i] = frequencyDic.get(i) + 1
            else:
                frequencyDic[i] = 1
        return sorted(frequencyDic.items(), key=lambda x: x[1], reverse=True)

    def __getTwoItemsFromDict(self, dict, type):
        if type == "filter size":
            self.SizeTwo = [dict[0], dict[1], dict[2], dict[3], dict[4]]
        else:
            self.StopWordTwo = [dict[0], dict[1], dict[2], dict[3], dict[4]]

    @staticmethod
    def __getValueByKey(self, data, key):
        val = list(data.keys())[list(data.values()).index(key)]
        return val







