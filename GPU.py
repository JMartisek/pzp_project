import time

import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
from CPU_one_thread import OneThreadCPU
import murmurHash

def filterSizeWords(data_keys, data_values,hashDic, min_length, max_length):
    hashed = list(data_keys)
    length = list(data_values)
    nData = np.array(hashed, dtype=np.uint64)
    nDataLength = np.array(length, dtype=np.uint8)
    sizeOfArray = nData.size
    output = np.zeros(sizeOfArray, dtype=np.uint64)

    BLOCK_SIZE = 256
    GRID_SIZE = (sizeOfArray + BLOCK_SIZE - 1) // BLOCK_SIZE

    # CUDA kernel
    kernel_code = """
    __global__ void search_words_kernel(const int64_t *hash_values, const uint8_t *word_lengths, int num_words, int min_length, int max_length, int64_t *results) {
        int tid = blockIdx.x * blockDim.x + threadIdx.x;

        if (tid < num_words) {
            int word_length = word_lengths[tid];
            if (word_length > min_length && word_length < max_length) {
                results[tid] = hash_values[tid];
            }
        }
    }
    """

    mod = SourceModule(kernel_code)
    search_Stopwords = mod.get_function("search_words_kernel")

    # Převod dat na GPU
    start2 = time.time()
    nData_gpu = cuda.to_device(nData)
    nDataLength_gpu = cuda.to_device(nDataLength)
    output_gpu = cuda.to_device(output)
    start = time.time()
    # Spuštění kernelu
    search_Stopwords(nData_gpu, nDataLength_gpu, np.int32(sizeOfArray), np.int32(min_length), np.int32(max_length), output_gpu, block=(BLOCK_SIZE, 1, 1), grid=(GRID_SIZE, 1, 1))
    stop = time.time()
    # Převod dat zpět na CPU
    cuda.memcpy_dtoh(output, output_gpu)
    stop2 = time.time()
    # Výpis výsledků
    realOutput = []
    print("GPU only process:", stop - start, "seconds \n GPU with data transfer between CPU and GPU:", stop2 - start2, "Seconds" )
    print("Data loading takes:", (stop2-start2)-(stop-start), "seconds.")
    complete = []
    realOutput = [hashDic.get(hash_value) for hash_value in output]
    for i in realOutput:
        if i != None:
            complete.append(i)
    print("Number of filtered words:", len(complete))
    print(output[:sizeOfArray])

# Příklad použití
"""
random_numbers = np.random.randint(0, 10, size=100)
data = open("data.txt", "r")
data = data.read()
parsedData = OneThreadCPU.parseWords(data)
Hash_lenght_dict = murmurHash.createHashLenght(parsedData)
Hash_word_dict = murmurHash.createHashWord(parsedData)
hashed = list(Hash_lenght_dict.keys())
length = list(Hash_lenght_dict.values())
print(random_numbers)
filterSizeWords(hashed, length, 5, 7)
"""