# top-graphs
Creates a graphical representation from the output of the Linux top command using mainly Matplotlib. A focus is put on memory, CPU, and pageins.

## Setup

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


## example output
![example graph from top output](example-graph.png)
