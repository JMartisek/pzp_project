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
    start2 = time.time()
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
    #print("GPU only process:", stop - start, "seconds \n GPU with data transfer between CPU and GPU:", stop2 - start2, "Seconds" )
    #print("Data loading takes:", (stop2-start2)-(stop-start), "seconds.")
    complete = []
    realOutput = [hashDic.get(hash_value) for hash_value in output]
    for i in realOutput:
        if i != None:
            complete.append(i)
    #print("Number of filtered words:", len(complete))
    sortedComplete = __wordsFrequency(complete)
    #print(output[:sizeOfArray])
    return [__getTwoItemsFromDict(sortedComplete), stop2 - start2]

def filterStopWords(data, stopWords,hashDic):
    large_array = np.array(data, dtype=np.int64)
    small_array = np.array(stopWords, dtype=np.int64)
    max_value = max(small_array)
    # Vytvoření pole pro výsledky
    result_array = np.zeros_like(large_array, dtype=np.bool_)
    start = time.time()
    # Převod na GPU
    large_array_gpu = cuda.to_device(large_array)
    small_array_gpu = cuda.to_device(small_array)
    result_array_gpu = cuda.to_device(result_array)

    # Spuštění jádra
    BLOCK_SIZE = 256
    GRID_SIZE = (large_array.size + BLOCK_SIZE - 1) // BLOCK_SIZE
    kernel_code = """
    __global__ void search_and_update_kernel(const int *large_array, int large_size, const int *small_array, int small_size, bool *result_array) {
        int tid = blockIdx.x * blockDim.x + threadIdx.x;

        if (tid < large_size) {
            int current_value = large_array[tid];


            for (int i = 0; i < small_size; ++i) {
                if (current_value == small_array[i]) {
                    result_array[tid] = true;
                    break;  
                }
            }
        }
    }
    """
    mod = SourceModule(kernel_code)
    search_and_update_kernel = mod.get_function("search_and_update_kernel")
    search_and_update_kernel(large_array_gpu, np.int32(large_array.size), small_array_gpu, np.int32(small_array.size),
                             result_array_gpu, block=(BLOCK_SIZE, 1, 1), grid=(GRID_SIZE, 1, 1))

    # Převod zpět na CPU
    cuda.memcpy_dtoh(result_array, result_array_gpu)
    realOutput = [hashDic.get(hash_value) for hash_value in data]
    result = pickStopWords(result_array,realOutput)

    stop = time.time()

    sortedResult = __wordsFrequency(result)
    # Výpis výsledků
    #print(result_array)
    return [__getTwoItemsFromDict(sortedResult),stop - start ]

def pickStopWords(booleanArray, data):
    output = []
    for i in range(len(data)):
        if booleanArray[i] == True:
            output.append(data[i])
    return output


def __wordsFrequency(data):
    frequencyDic = {}
    for i in data:
        if i in frequencyDic:
            frequencyDic[i] = frequencyDic.get(i) +1
        else:
            frequencyDic[i] = 1
    # bogosort.bogoPogoSort(list(frequencyDic.values()))
    return sorted(frequencyDic.items(), key=lambda x: x[1], reverse=True)

def __getTwoItemsFromDict(dict):
    return [dict[0], dict[1]]


