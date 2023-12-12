import sys
import time

import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
from CPU_one_thread import OneThreadCPU
import murmurHash


def filterSizeWords(inputData, dataLenght, hashDic, min_length, max_length):
    nData = np.array(inputData, dtype=np.uint64)
    nDataLength = np.array(dataLenght, dtype=np.uint8)
    sizeOfArray = nData.size
    output = np.zeros(sizeOfArray, dtype=np.uint64)

    BLOCK_SIZE = 256
    GRID_SIZE = (sizeOfArray + BLOCK_SIZE - 1) // BLOCK_SIZE


    kernel_code = """
    __global__ void filterStopWords(const int64_t *hash_values, const uint8_t *word_lengths, int num_words, int min_length, int max_length, int64_t *results) {
        int tid = blockIdx.x * blockDim.x + threadIdx.x;

        if (tid < num_words) {
            int word_length = word_lengths[tid];
            if (word_length > min_length && word_length < max_length) {
                results[tid] = hash_values[tid];
            }
        }
        __syncthreads();
    }
    """

    start = time.time()
    mod = SourceModule(kernel_code)
    search_Stopwords = mod.get_function("filterStopWords")

    nData_gpu = cuda.to_device(nData)
    nDataLength_gpu = cuda.to_device(nDataLength)
    output_gpu = cuda.to_device(output)
    search_Stopwords(nData_gpu, nDataLength_gpu, np.int32(sizeOfArray), np.int32(min_length), np.int32(max_length), output_gpu, block=(BLOCK_SIZE, 1, 1), grid=(GRID_SIZE, 1, 1))

    cuda.memcpy_dtoh(output, output_gpu)
    complete = []
    realOutput = [hashDic.get(hash_value) for hash_value in output]
    for i in realOutput:
        if i != None:
            complete.append(i)
    stop = time.time()
    sortedComplete = __wordsFrequency(complete)
    return [__getTwoItemsFromDict(sortedComplete), stop - start]


def filterStopWords(data, stopWords,hashDic):
    nData = np.array(data, dtype=np.uint64)
    nStopWords = np.array(stopWords, dtype=np.uint64)
    result_array = np.zeros_like(nData, dtype=np.bool_)



    BLOCK_SIZE = 256
    GRID_SIZE = (nData.size + BLOCK_SIZE - 1) // BLOCK_SIZE


    kernel_code = """
    __global__ void search_and_update_kernel(const uint64_t *nData, int dataLenght, const uint64_t *nStopWords, int numberOfStopWords, bool *result_array) {
        int tid = blockIdx.x * blockDim.x + threadIdx.x;

        if (tid < dataLenght) {
            uint64_t current_value = nData[tid];

            for (int i = 0; i < numberOfStopWords; ++i) {
                if (current_value == nStopWords[i]) {
                    result_array[tid] = true;
                    break;  
                }
            }
        }
        __syncthreads();
    }
    """

    start = time.time()
    mod = SourceModule(kernel_code)
    search_and_update_kernel = mod.get_function("search_and_update_kernel")

    nData_gpu = cuda.to_device(nData)
    nStopWords_gpu = cuda.to_device(nStopWords)
    result_array_gpu = cuda.to_device(result_array)
    search_and_update_kernel(nData_gpu, np.uint64(nData.size), nStopWords_gpu, np.uint64(nStopWords.size),
                             result_array_gpu, block=(BLOCK_SIZE, 1, 1), grid=(GRID_SIZE, 1, 1))

    cuda.memcpy_dtoh(result_array, result_array_gpu)
    realOutput = [hashDic.get(hash_value) for hash_value in data]
    result = pickStopWords(result_array,realOutput)

    stop = time.time()
    sortedResult = __wordsFrequency(result)
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
    return sorted(frequencyDic.items(), key=lambda x: x[1], reverse=True)


def __getTwoItemsFromDict(myDictionary):
    return [myDictionary[0], myDictionary[1]]


