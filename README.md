# top-graphs
Get a graphical representation from the output of the Unix/Linux top command for a specific process.

## Setup
Note: Setup instruction aimed for Unix/Linux machines.
### Part 1: Get your data
1. Enter the following in terminal to output data from the top command:
```
top | grep PROCESSNAME > OUTPUTTEXTFILE.txt
```
Example:
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

2. Run the following command in terminal (do not include .txt and remember to include the slash at the end of the path name!)
```
python3 main.py topoutputfilename /path/to/my/topoutputfile/
```
Example (if you named your top output file "video-call-intervals" and you saved that file in "/Users/cpqa/"):
```
python3 main.py video-call-intervals /Users/cpqa/
```
Note: An interactive graph will pop-up and when you close that window, an Excel file will be generated and saved in the same directory as your top output text file.


## Example Output Graph
![example graph from top output](example-graph.png)
