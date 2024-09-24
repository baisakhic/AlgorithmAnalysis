import timeit
from datetime import datetime
from time import process_time

sortedData = ''


def inPlaceInsertionSort(input_arr):
	global sortedData
	input_length = len(input_arr)
	for i in range(1, input_length):
		insert_ele = input_arr[i]
		pos = i - 1
		dateTimeLeft = datetime.fromisoformat(input_arr[pos].split(b' ')[0].decode('utf-8'))
		dateTimeRight = datetime.fromisoformat(insert_ele.split(b' ')[0].decode('utf-8'))
		dateTimeLeftInt = int(dateTimeLeft.timestamp())
		dateTimeRightInt = int(dateTimeRight.timestamp())
		# while pos >= 0 and dateTimeLeft > dateTimeRight:
		while pos >= 0 and dateTimeLeftInt > dateTimeRightInt:
			input_arr[pos + 1] = input_arr[pos]
			pos = pos - 1
			dateTimeLeft = datetime.fromisoformat(input_arr[pos].split(b' ')[0].decode('utf-8'))
			dateTimeLeftInt = int(dateTimeLeft.timestamp())
		input_arr[pos + 1] = insert_ele

	sortedData = input_arr

def insertionSortRun(content):
	# start = time.time()
	# inPlaceInsertionSort(content)
	time_taken = timeit.timeit(stmt="inPlaceInsertionSort(content)", setup="from __main__ import inPlaceInsertionSort, content", number=1,  timer=process_time)

	# end = time.time()
	# time_taken = end - start
	return sortedData, time_taken

