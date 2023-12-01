
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

    __privateVariable = 0

    def __init__(self, hashed, data, stopWords):
        print("CPU one thread is starting ...")
        self.data = data
        self.stopWords = stopWords
        if not hashed:
            OneThreadCPU.__filterSizeWord(self)
            OneThreadCPU.__stopWordsFilter(self)
            self.countStopWordDict = OneThreadCPU.__wordsFrequency(self, self.indexStopWordsDict.values())
            OneThreadCPU.__getTwoItemsFromDict(self,self.countStopWordDict, "stop word")
            self.countSizeWordDict = OneThreadCPU.__wordsFrequency(self, self.middleValue)
            OneThreadCPU.__getTwoItemsFromDict(self,self.countSizeWordDict, "word size")

        else:
            print("Not ready yet..")
        # vsechny vystupy jako instance classy, tedy: 3 pole a v kazdem rozdeleni do delky slov

    @staticmethod
    def parseWords(array):
        return OneThreadCPU.__cleanWords(array.split())

    @staticmethod
    def __checkLen(word):
        if(len(word) == 0):
            return False
        return True

    @staticmethod
    def __weirdStringParser(list, word, index):
        partioned = word.partition("--")
        list[index] = partioned[0]
        list.insert(index+1,partioned[2])
        return list

    @staticmethod
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

    @staticmethod
    def __filterSizeWord(self):
        for word in self.data:
            if len(word) > 7:
                OneThreadCPU.greaterThen8.append(word)
            elif len(word) < 5:
                OneThreadCPU.lessThen4.append(word)
            else:
                OneThreadCPU.middleValue.append(word)
        print("Number of elements after word lenght filtration: ",len(self.middleValue))

    @staticmethod
    def __stopWordsFilter(self):
        for index, word in enumerate(self.data):
            if word in self.stopWords:
                self.indexStopWordsDict[index] = word
        print("Number of elements after stop word filtration: ", len(self.indexStopWordsDict.values()))

    @staticmethod
    def __wordsFrequency(self, data):
        frequencyDic = {}
        for i in data:
            if i in frequencyDic:
                frequencyDic[i] = frequencyDic.get(i) +1
            else:
                frequencyDic[i] = 1
        # bogosort.bogoPogoSort(list(frequencyDic.values()))
        return sorted(frequencyDic.items(), key=lambda x: x[1], reverse=True)

    def __getTwoItemsFromDict(self, dict, type):
        print("First",type," value", dict[0],  "and second", dict[1])


    @staticmethod
    def __getValueByKey(self, data, key):
        val = list(data.keys())[list(data.values()).index(key)]
        return val







