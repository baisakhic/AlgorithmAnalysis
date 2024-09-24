#!/usr/bin/env python3
import os
import argparse
import sys
from time import process_time
from datetime import datetime
from mergesort import mergeSortRun, mergeSort
from insertion import insertionSortRun, inPlaceInsertionSort
from sort_3 import timSortRun, tim_sort2
import csv, timeit
from plot_daa import plot_graph
import matplotlib.pylab as plt

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = dir_path + "/bin/input"
output_path = dir_path + "/bin/output"
choices = ['mergesort', 'insertionsort', 'timsort']
output = []
header = ['Algorithm', 'Execution No', 'File Type', 'Lines', 'Time to Read File', 'Sort Time']
filename = ""
content = ""
output.append(header)
run = 15
output_file = 'statistics_new.csv'


def readFile():
    with open(filename, 'rb') as f:
        global content
        content = f.readlines()


def sortAlgo(algo, dataset):
    if not algo:
        print("Executing All")
        algo = choices
    else:
        print("Algo Chosen: " + algo)
        algo = [algo]

    for a in algo:
        list = [o for o in os.listdir(input_path) if os.path.isdir(os.path.join(input_path,o))]
        for foldername in list:
            if dataset and not foldername.__contains__(dataset):
                continue
            input_folder = input_path + "/" + foldername
            fileList = os.listdir(input_folder)
            fileList.sort(key=lambda x: int(x.split('.')[0]))
            for f in fileList:
                global filename
                filename = input_folder + "/" + f
                for i in range(run):
                    print("Run : " + i.__str__() + " :: file : " + filename)
                    # t = timeit.Timer(readFile)
                    timeToRead = timeit.timeit(stmt="readFile()", setup="from __main__ import readFile", number=1, timer=process_time)
                    sortedData = ''
                    if 'merge' in a:
                        sortedData, timeToRun = mergeSortRun(content)
                    elif 'insert' in a:
                        sortedData, timeToRun = insertionSortRun(content)
                    elif 'tim' in a:
                        sortedData, timeToRun = timSortRun(content)
                    row = [a, i, foldername, int(f.split('.')[0]), float(timeToRead), float(timeToRun)]
                    output.append(row)
                    with open(output_path + "/" + output_file, 'a+', newline='') as csvfile:
                        spamwriter = csv.writer(csvfile, delimiter=',')
                        spamwriter.writerow(row)
                    test(sortedData)
                    write(foldername, f, sortedData, a)


def test(sortedData):
    prevDateTime = None
    for line in sortedData:
        dateTime = datetime.fromisoformat(line.split(b' ')[0].decode('utf-8'))
        if prevDateTime and prevDateTime > dateTime:
            print("Error in Sort :: Previous Date Time = " + prevDateTime.strftime("%m/%d/%Y, %H:%M:%S") + " : Current Date Time = " + dateTime.strftime("%m/%d/%Y, %H:%M:%S"))
            break
        prevDateTime = dateTime



def write(folder, filename, content, a):
    output_folder = output_path + "/" + a + "/" + folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    outputfile = output_folder + "/" + filename
    with open(outputfile, 'wb') as f:
        f.writelines(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", help="Input Folder Path")
    parser.add_argument("-o", "--output", help="Output Folder Path")
    parser.add_argument("-d", "--dataset", choices=['A', 'B', 'C'], help="Output Folder Path")
    parser.add_argument('-s', '--sort', choices=choices,
                        help='Sorting Algorithms. Choose \'mergesort\', \'insertionsort\' or \'timsort\'')
    parser.add_argument('-r', '--run', type=int,
                        help='Number of runs per sort')
    parser.add_argument('-t', '--type', choices=['sort', 'plot', 'both'],
                        help='Type of Operation. Choose \'sort\', \'plot\' or \'both\'. Default choice is both.')

    args = parser.parse_args()

    if args.input:
        input_path = args.input

    if args.output:
        output_path = args.output

    if args.run:
        run = args.run

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    if not os.path.exists(output_path + "/" + output_file):
        with open(output_path + "/statistics_new.csv", 'w+', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(header)

    if not args.type or (args.type and not args.type == 'plot'):
        sortAlgo(args.sort, args.dataset)
    if not args.type or (args.type and not args.type == 'sort'):
        plot_graph(args.sort, args.dataset)



