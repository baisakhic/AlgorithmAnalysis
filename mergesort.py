from time import process_time
from datetime import datetime
import timeit

binary_space = ''.join(format(ord(' '), '08b'))
sortedData = ''

def mergeSort(input_arr) :
	global sortedData
	input_length = len(input_arr)
	if input_length >= 2:
		i = 0
		j = 0
		k = 0
		midpoint = int(input_length/2)
		left_arr = input_arr[:midpoint]
		right_arr = input_arr[midpoint:]
		left_arr = mergeSort(left_arr)
		right_arr = mergeSort(right_arr)
		len_left = len(left_arr)
		len_right = len(right_arr)
		result = []
		while i < len_left and j < len_right:
			dateTimeLeft = datetime.fromisoformat(left_arr[i].split(b' ')[0].decode('utf-8'))
			dateTimeRight = datetime.fromisoformat(right_arr[j].split(b' ')[0].decode('utf-8'))
			dateTimeLeftInt = int(dateTimeLeft.timestamp())
			dateTimeRightInt = int(dateTimeRight.timestamp())
			if dateTimeLeftInt < dateTimeRightInt:
				result.append(left_arr[i])
				i = i + 1
			else:
				result.append(right_arr[j])
				j = j + 1
			k = k + 1

		while i < len_left:
			result.append(left_arr[i])
			i = i + 1
			k = k + 1
		while j < len_right:
			result.append(right_arr[j])
			j = j + 1
			k = k + 1
		#To return value when using timeit
		sortedData = result
		return result
	#To return value when using timeit

	sortedData = input_arr
	return input_arr

def mergeSortRun(content):
	# start = time.time()
	# mergeSort(content)
	time_taken = timeit.timeit(stmt="mergeSort(content)", setup="from __main__ import mergeSort, content", number=1,  timer=process_time)
	# end = time.time()
	# time_taken = end-start
	return sortedData, time_taken
