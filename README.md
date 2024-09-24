# CSC 505 - Project 1

## Steps to Build Project
**Step 1:** Clone the code to your local machine
```
git clone <repo URL>
```

**Step 2:** Install Requirements
```
pip install -r requirements.txt
```

## Usage
```
./sortData [-s sort] [-d dataset] [-r number of runs] [-t type] [-i input folder] [-o output folder]
or
./sortData
or
./sordData -s mergesort -d A
or
./sordData -s mergesort -d A -t plot
or
./sortData -r 15
```

### Arguments

```
-s --sort		Choose which sort to run. Choices are 'mergesort, 'insertionsort' and 'timsort'. Runs all three sorts by default. 
-d --dataset            Chooses which folder to sort data. Choices are 'A', 'B' and 'C'. Sort Data in All Folders by default. 
-r --run		Specify number of executions (including warmup). Default = 15
-t --type		Either Sort Data, Plot already sorted data or both. Choices are 'sort', 'plot' and 'both' 
-i --input		Specifies the folder where the input files are located. By default, the program looks in /bin/input
-o --output		Specifies the folder where the output files are saved. By default, the program saves in /bin/output
```

### Default Requirement of Folder Structure
```
CSC505-P1-Sort/
├── bin/
│   ├── input/
│   │   ├── A/
│   │   │   └── <log files>
│   │   ├── B/
│   │   │   └── <log files>
│   │   └── C/
│   │       └── <log files>
│   └── output/
│       ├── mergesort/ 
│       │   ├── A/
│       │   │   └── <sorted log files>
│       │   ├── B/
│       │   │   └── <sorted log files>
│       │   └── C/
│       │       └── <sorted log files>
│       ├── insertionsort/ 
│       │   ├── A/
│       │   │   └── <sorted log files>
│       │   ├── B/
│       │   │   └── <sorted log files>
│       │   └── C/
│       │       └── <sorted log files>
│       ├── timsort/ 
│       │   ├── A/
│       │   │   └── <sorted log files>
│       │   ├── B/
│       │   │   └── <sorted log files>
│       │   └── C/
│       │       └── <sorted log files>
│       ├── graph/
│       │   └── <plots>
│       └── statistics_new.csv
├── sortData.py
├── insertion.py
├── mergesort.py
├── sort_3.py
└── plot_daa.py
```

## References for writing the code

1. Insertion Sort Algorithm: https://www.geeksforgeeks.org/python-program-for-insertion-sort/
2. Merge Sort Algorithm: https://www.geeksforgeeks.org/merge-sort/
3. Tim Sort Algorithm: https://www.pythonpool.com/python-timsort/  https://www.geeksforgeeks.org/timsort/ 
