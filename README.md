# top-graphs
Creates a graphical representation from the output of the Linux top command using mainly Matplotlib. A focus is put on memory, CPU, and pageins.

## Setup
Note: Setup instruction aimed for Unix/Linux machines, but can be easily adapted for Windows machines.
### Part 1: Get your data
1. Enter the following in terminal to output data from the top command:
```
top | grep PROCESSNAME > OUTPUTTEXTFILE.txt
```
For example:
```
top | grep Bria\ Enterprise > video-call-intervals.txt
```

2. Ctrl + C to stop outputting data to your text file.


### Part 2: Setup the environment
1. Install python3 using [Homebrew](https://brew.sh) for Mac or download from [here](https://www.python.org/downloads/windows/).

2. [Clone](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) this repo onto your machine.

3. Install the dependencies.
```
pip3 install -r requirements.txt
```

### Part 2: Convert the data into graphs
1. Navigate to directory containing **main.py** in your terminal.
Example:
```
cd path/to/main/
```
2. Run the following command in terminal (do not include .txt)
```
python3 main.py outputfilename /path/to/my/outputfile/
```
Example:
```
python3 main.py video-call-intervals /Users/cpqa/
```
Note: The resulting Excel file will be saved in the same directory as your text file containing the top output data.


## Example Output Graph
![example graph from top output](example-graph.png)
