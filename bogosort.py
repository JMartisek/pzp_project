from random import shuffle

def bogoPogoSort(data):
    while not isSorted(data):
        shuffle(data)
    return data


def isSorted(data):
    for i in range(len(data)-1):
        if data[i] < data[i+1]:
            return False
    return True
