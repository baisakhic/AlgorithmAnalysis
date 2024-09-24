#!/usr/bin/env python3
import csv, os, random
import math
import sys

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import argparse

choices = ['mergesort', 'insertionsort', 'timsort']
folders = ["A", "B", "C"]
input_path = ['bin/output/statistics_new.csv', 'bin/output/statistics_time_wall.csv']
output_path = 'bin/output/graph/'

def log_fit(x, a, c):
    return x * np.log(x) * a + c


def square_fit(x, a, b, c):
    return a * x * x + b * x + c

def square_curve(plot_data, y_new):
    max_x = np.max([i for i in plot_data.keys()])
    max_y = np.max([i for i in y_new])
    x = np.linspace(0, max_x, 50)
    divisor = x[49] * x[49] / max_y
    y = [i * i / divisor for i in x]
    return x, y

def log_curve(plot_data, y_new):
    max_x = np.max([i for i in plot_data.keys()])
    max_y = np.max([i for i in y_new])
    x = np.linspace(0, max_x, 50)
    divisor = x[49] * np.log(x[49]) / max_y
    y = []
    for i in x:
        if i == 0:
            y.append(0)
            continue
        y.append(i * np.log(i)/divisor)
    return x, y


def get_warm_up(total_runs):
    if total_runs >= 15:
        return 5
    elif total_runs >= 10:
        return 2
    elif total_runs >= 4:
        return 1
    else:
        return 0

def plot_graph(sorts, file_types):
    fig, ax = plt.subplots()
    handles = []
    first = False
    if not sorts:
        print("Plotting All Sorts")
        sorts = choices
    else:
        print("Sort Chosen: " + sorts)
        sorts = [sorts]

    if not file_types:
        print("Plotting All File Types")
        file_types = folders
    else:
        print("File Type Chosen: " + file_types)
        file_types = [file_types]
    for input in input_path:
        for sort in sorts:
            for file_type in file_types:

                dataType = ""

                if file_type == 'A':
                    dataType = "Random Order"
                elif file_type == 'B':
                    dataType = "Reverse Order"
                else:
                    dataType = "Sorted Order"

                if 'merge' in sort:
                    dataType = "Merge Sort - " + dataType
                elif 'insert' in sort:
                    dataType = "Insertion Sort - " + dataType
                else:
                    dataType = "Tim Sort - " + dataType

                input_folder = 'bin/input/' + file_type
                fileList = os.listdir(input_folder)
                fileList.sort(key=lambda x: int(x.split('.')[0]))
                fileList = [i.split('.')[0] for i in fileList]

                result = {}
                resultRuns = {}

                data = []
                totalRuns = 0
                with open(input, newline='') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                    for row in spamreader:
                        if (row[0] == sort and row[2] == file_type):
                            data.append(row)
                            if row[3] in fileList:
                                fileList.remove(row[3])
                            if row[3] in resultRuns.keys():
                                resultRuns[row[3]] = resultRuns[row[3]] + 1
                            else:
                                resultRuns[row[3]] = 1


                if not data:
                    continue

                for row in data:
                    if int(row[1]) < get_warm_up(resultRuns[row[3]]):
                        continue
                    if row[3] in result.keys():
                        result[row[3]] = [(result[row[3]][0] + float(row[5])), (result[row[3]][1] + 1)]
                    else:
                        result[row[3]] = [float(row[5]), 1]

                plot_data = {}
                plot_data_estimate = {}
                for key in result.keys():
                   plot_data[int(key)] = float(result[key][0] / result[key][1])
                   plot_data_estimate[int(key)] = float(result[key][0] / result[key][1])

                # fig, ax = plt.subplots()

                y_new = []
                y_new_estimate = []

                if sort == "timsort":
                    popt, _ = curve_fit(log_fit, np.array(list(plot_data.keys())), np.array(list(plot_data.values())))
                    a, c = popt
                    y_new = log_fit(list(plot_data.keys()), a, c)
                    if fileList:
                        for i in fileList:
                            plot_data_estimate[int(i)] = -1
                        y_new_estimate = square_fit(np.array(list(plot_data_estimate.keys())), a, b, c)
                else:
                    popt, _ = curve_fit(square_fit, np.array(list(plot_data.keys())), np.array(list(plot_data.values())))
                    a, b, c = popt
                    y_new = square_fit(np.array(list(plot_data.keys())), a, b, c)
                    if fileList:
                        for i in fileList:
                            plot_data_estimate[int(i)] = -1
                        y_new_estimate = square_fit(np.array(list(plot_data_estimate.keys())), a, b, c)

                y_new_sorted = [x for _,x in sorted(zip(plot_data_estimate, y_new))]

                if 'wall' in input:
                    color = 'r'
                    label = "Wall Clock Time"
                else:
                    color = 'b'
                    label = "Process Clock Time"

                points = ax.scatter(*zip(*sorted(plot_data.items())), label="Data Points for " + label, color=color, edgecolor = 'k')
                fited_curve = ax.plot(np.array(list(sorted(plot_data.keys()))), y_new_sorted, color=color, label="Fitted Curve for " + label)
                # ax.legend(handles=[points, fited_curve[0]])
                handles.append(points)
                handles.append(fited_curve[0])

                if not os.path.exists(output_path):
                    os.mkdir(output_path)

                plt.xlabel("No of Lines")
                plt.ylabel("Time Taken in Seconds")
                plt.title(dataType)

                # plt.savefig(output_path + file_type + "_" + sort)

                if False:
                    x_diff = [int(i) for i in fileList]
                    y_diff = []
                    for i in y_new_estimate:
                        if i not in y_new:
                            y_diff.append(i)
                    fig, ax = plt.subplots()

                    y_new_estimate_sorted = [x for _,x in sorted(zip(plot_data_estimate, y_new_estimate))]


                    points = ax.scatter(*zip(*sorted(plot_data.items())), label="Data Points for " + dataType, color='r', edgecolor='k')
                    points2 = ax.scatter(x_diff, y_diff, label="Estimated Data Points for " + dataType, color='y', edgecolor='k')
                    fited_curve = ax.plot(np.array(list(sorted(plot_data_estimate.keys()))), y_new_estimate_sorted, color='b', label="Fitted Curve for " + dataType)
                    ax.legend(handles=[points, points2, fited_curve[0]])

                    plt.xlabel("No of Lines")
                    plt.ylabel("Time Taken in Seconds")
                    plt.title(dataType)

                    plt.savefig(output_path + file_type + "_" + sort + "_withEstimate")
    ax.legend(handles=handles)
    plt.show()

def plot_file_data(sorts, file_types):
    if not sorts:
        print("Plotting All Sorts")
        sorts = choices
    else:
        print("Sort Chosen: " + sorts)
        sorts = [sorts]

    if not file_types:
        print("Plotting All File Types")
        file_types = folders
    else:
        print("File Type Chosen: " + file_types)
        file_types = [file_types]

    for sort in sorts:
        for file_type in file_types:

            dataType = ""

            if file_type == 'A':
                dataType = "Random Order"
            elif file_type == 'B':
                dataType = "Reverse Order"
            else:
                dataType = "Sorted Order"

            if 'merge' in sort:
                dataType = "Merge Sort - " + dataType
            elif 'insert' in sort:
                dataType = "Insertion Sort - " + dataType
            else:
                dataType = "Tim Sort - " + dataType

            result = {}
            resultRuns = {}

            data = []
            totalRuns = 0
            with open(input_path, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    if (row[0] == sort and row[2] == file_type):
                        data.append(row)
                        if row[3] in resultRuns.keys():
                            resultRuns[row[3]] = resultRuns[row[3]] + 1
                        else:
                            resultRuns[row[3]] = 1


            if not data:
                continue

            for row in data:
                if row[3] in result.keys():
                    result[row[3]] = [(result[row[3]][0] + float(row[4])), (result[row[3]][1] + 1)]
                else:
                    result[row[3]] = [float(row[4]), 1]

            plot_data = {}
            plot_data_estimate = {}
            for key in result.keys():
               plot_data[int(key)] = float(result[key][0] / result[key][1])
               plot_data_estimate[int(key)] = float(result[key][0] / result[key][1])

            fig, ax = plt.subplots()

            points = ax.scatter(*zip(*sorted(plot_data.items())), label="Data Points for " + dataType, color='r', edgecolor = 'k')
            ax.legend(handles=[points])

            if not os.path.exists(output_path):
                os.mkdir(output_path)

            plt.xlabel("No of Lines")
            plt.ylabel("Time Taken in Seconds")
            plt.title(dataType)

            plt.savefig(output_path + "file_read_"+file_type + "_" + sort)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", choices=['A', 'B', 'C'], help="Output Folder Path")
    parser.add_argument('-s', '--sort', choices=choices,
                        help='Sorting Algorithms. Choose \'mergesort\', \'insertionsort\' or \'timsort\'')

    args = parser.parse_args()

    plot_graph(args.sort, args.dataset)
    plot_file_data(args.sort, args.dataset)
