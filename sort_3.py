import timeit
from datetime import datetime
from time import process_time


MINIMUM = 32
sortedData = ''
 
def getMinrun(n):
    r = 0
    while n >= MINIMUM: 
        r |= n & 1
        n >>= 1
    return n + r

def insertionSort(array, left, right):
    for i in range(left + 1,right + 1):
        element = array[i]
        j = i - 1
        dateTimeLeft = element.split(b' ')[0].decode('utf-8')
        dateTimeRight = array[j].split(b' ')[0].decode('utf-8')
        while datetime.fromisoformat(dateTimeLeft) < datetime.fromisoformat(dateTimeRight) and j >= left:
            array[j + 1] = array[j]
            j = j - 1
        array[j + 1] = element
    return array
              
def merge(array, l, m, r):
    i = 0
    j = 0
    k = l

    left_len = m - l + 1
    right_len = r - m
    left = []
    right = []

    for i in range(0, left_len):
        left.append(array[l + i])
    for i in range(0, right_len):
        right.append(array[m + 1 + i])

    while j < right_len and  i < left_len :
        dateTimeLeft = left[i].split(b' ')[0].decode('utf-8')
        dateTimeRight = right[j].split(b' ')[0].decode('utf-8')

        if datetime.fromisoformat(dateTimeLeft) <= datetime.fromisoformat(dateTimeRight):
            array[k] = left[i]
            i = i + 1
            k = k + 1
        else:
            array[k] = right[j]
            j = j + 1
            k = k + 1

    while i < left_len:
        array[k] = left[i]
        i = i + 1
        k = k + 1

    while j < right_len:
        array[k] = right[j]
        j = j + 1
        k = k + 1
    sortedData = array

def tim_sort(array):
    global sortedData
    input_length = len(array)
    minrun = getMinrun(input_length)

    for start in range(0, input_length, minrun):
        end = min(start + minrun - 1, input_length - 1) 
        insertionSort(array, start, end)

    size = minrun 
    while size < input_length: 
        for left in range(0, input_length, 2 * size):  
            mid = min(input_length - 1, left + size - 1) 
            right = min((left + 2 * size - 1), (input_length - 1))

            merge(array, left, mid, right)
        size = 2 * size 
    sortedData = array


def fitness(line):
    dateTime = datetime.fromisoformat(line.split(b' ')[0].decode('utf-8'))
    dateTimeInt = int(dateTime.timestamp())
    return dateTimeInt


def tim_sort2(content):
    global sortedData
    content = sorted(content, key=lambda x: fitness(x))
    sortedData = content


def timSortRun(content):
    # start = time.time()
    # tim_sort(content)
    time_taken = timeit.timeit(stmt="tim_sort2(content)", setup="from __main__ import tim_sort2, content", number=1,  timer=process_time)
    # end = time.time()
    # time_taken = end-start
    return sortedData, time_taken
