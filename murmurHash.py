def bytes_to_long(bytes):
    length = len(bytes)
    if length < 8:
        extra = 8 - length
        bytes = b'\000' * extra + bytes
    assert len(bytes) == 8
    return sum((b << (k * 8) for k, b in enumerate(bytes)))


def murmur64(data, seed = 19820125):

    m = 0xc6a4a7935bd1e995
    r = 47

    MASK = 2 ** 64 - 1

    data_as_bytes = bytearray(data, encoding='utf-8')

    h = seed ^ ((m * len(data_as_bytes)) & MASK)

    off = int(len(data_as_bytes)/8)*8
    for ll in range(0, off, 8):
        k = bytes_to_long(data_as_bytes[ll:ll + 8])
        k = (k * m) & MASK
        k = k ^ ((k >> r) & MASK)
        k = (k * m) & MASK
        h = (h ^ k)
        h = (h * m) & MASK

    l = len(data_as_bytes) & 7

    if l >= 7:
        h = (h ^ (data_as_bytes[off+6] << 48))

    if l >= 6:
        h = (h ^ (data_as_bytes[off+5] << 40))

    if l >= 5:
        h = (h ^ (data_as_bytes[off+4] << 32))

    if l >= 4:
        h = (h ^ (data_as_bytes[off+3] << 24))

    if l >= 3:
        h = (h ^ (data_as_bytes[off+2] << 16))

    if l >= 2:
        h = (h ^ (data_as_bytes[off+1] << 8))

    if l >= 1:
        h = (h ^ data_as_bytes[off])
        h = (h * m) & MASK

    h = h ^ ((h >> r) & MASK)
    h = (h * m) & MASK
    h = h ^ ((h >> r) & MASK)

    return h
def hashedArray(data):
    output =[]
    for i in data:
        output.append(murmur64(i))
    return output
def createHashLenght(data):
    MyTextDictionary = {}
    for i in data:
        MyTextDictionary[murmur64(i)] = len(i)
    return MyTextDictionary

def createHashWord(data):
    MyTextDictionary = {}
    for i in data:
        MyTextDictionary[murmur64(i)] = i
    return MyTextDictionary

def hashArray(data):
    output = []
    lenght = []
    for i in data:
        lenght.append(len(i))
        output.append(murmur64(i))
    return output,lenght