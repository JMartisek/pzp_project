from pycuda.compiler import SourceModule
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
from pycuda.autoinit import context
import numpy
import time
import math

#2560 cuda cores


def filterStopWords(stopWords,data ):

    nData = numpy.array(data, dtype=numpy.uint64)
    nStopWords = numpy.array(stopWords, dtype=numpy.uint64)
    sizeOfArray = nData.size
    word_array = numpy.zeros(len(nStopWords), dtype=numpy.bool_)
    word_index = numpy.zeros(len(nStopWords) * sizeOfArray, dtype=numpy.uint64)
    word_count = numpy.zeros(len(nStopWords), dtype=numpy.uint64)

    BLOCK_SIZE = 256
    GRID_SIZE= (sizeOfArray + BLOCK_SIZE - 1) // BLOCK_SIZE

    # CUDA kernel
    kernel_code = """
    __global__ void search_Stopwords(const int *input_array, int array_size, const int *hashes_of_words, int num_words, bool *word_found, int *word_positions, int *word_counts) {
        int tid = blockIdx.x * blockDim.x + threadIdx.x;
    
        if (tid < array_size) {
            int current_hash = input_array[tid];
    
            for (int i = 0; i < num_words; ++i) {
                if (current_hash == hashes_of_words[i]) {
                    int count = atomicAdd(&word_counts[i], 1); // Atomicky inkrement poctu vyskytu slova
                    word_positions[i * array_size + count] = tid; // Ulozime index v puvodnim poli
                    word_found[i] = true;
                }
            }
        }
    }
    """
    mod = SourceModule(kernel_code)
    search_Stopwords = mod.get_function("search_Stopwords")

    #alokace pameti gpu
    nData_gpu = cuda.mem_alloc(nData.nbytes)
    nStopWords_gpu = cuda.mem_alloc(nStopWords.nbytes)
    word_array_gpu = cuda.mem_alloc(word_array.nbytes)
    word_index_gpu = cuda.mem_alloc(word_index.nbytes)
    word_count_gpu = cuda.mem_alloc(word_count.nbytes)

    #kopirovani dat na gpu
    cuda.memcpy_htod(nData_gpu, nData)
    cuda.memcpy_htod(nStopWords_gpu, nStopWords)
    cuda.memcpy_htod(word_array_gpu, word_array)
    cuda.memcpy_htod(word_index_gpu, word_index)
    cuda.memcpy_htod(word_count_gpu, word_count)

    search_Stopwords(nData_gpu, numpy.int32(sizeOfArray), nStopWords_gpu, numpy.int32(len(nStopWords)),
                     word_array_gpu,word_index_gpu,word_count_gpu, block=(BLOCK_SIZE, 1, 1), grid=(GRID_SIZE, 1, 1))

    #kopirovani dat zpet na CPU
    cuda.memcpy_dtoh(word_array, word_array_gpu)
    cuda.memcpy_dtoh(word_index, word_index_gpu)
    cuda.memcpy_dtoh(word_count, word_count_gpu)
    # Výpis výsledků

    for i, found in enumerate(word_array):
        if found:
            word = nStopWords[i]
            positions = word_index[i * sizeOfArray: i * sizeOfArray + word_count[i]]
            print(f"Slovo s hashem {word} nalezeno na pozicích {positions}")
