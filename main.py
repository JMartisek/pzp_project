import matplotlib


def parseWords(array):
    return array.split()

def checkLen(word):
    if(len(word) == 0):
        return False
    return True
def weirdStringParser(list, word, index):
    partioned = word.partition("--")
    list[index] = partioned[0]
    list.insert(index+1,partioned[2])
    return list

def arrayCount(stopWords, data):
    counter = 0
    for i in data:
        if i in stopWords:
            counter +=1
    return counter

data = open("data.txt", "r")
data = data.read()
stopData = open("stop_words.txt", "r")
stopData = stopData.read()

mujList = parseWords(data)





#mujList = ["pepa.", "pepa--jede", "pepa,", "pepa\"", "pepa-", "pepa:"]
repeat = True
susWords = []
lastWordList = [",", ")", ".", "\"", "-", ":", ";", "!", "?"]
firstWordList = ["\"", "-", "("]
for index, a in enumerate(mujList):
    repeat = True

    while (repeat == True):
        repeat = False
        if checkLen(a) > 0:
            if a[len(a) - 1] in lastWordList:#== "," or a[0] == ")" or a[len(a) - 1] == "." or a[len(a) - 1] == "\"" or a[len(a) - 1] == "-" or a[len(a) - 1] == ":" or a[len(a) - 1] == ";" or a[len(a) - 1] == "!"or a[len(a) - 1] == "?":
                a = a[0:len(a) - 1]
                mujList[index] = a
                repeat = checkLen(a)

            elif a[0] in firstWordList:#== "\"" or a[0] == "-" or a[0] == "(":
                a = a[1:]
                mujList[index] = a
                repeat = checkLen(a)
            if "--" in a:
                mujList = weirdStringParser(mujList,a, index)
    #print(a)
#print(mujList)

print("Number of arrays: ", arrayCount(stopData, mujList))
