# DESCRIPTION:
# Converts top output in a text file into a graphical format.

# READ ME BEFORE EXECUTING:
# - Make sure to use this command: top | grep Bria\ Enterprise >> <filename>.txt 
#     -- modifying the command by adding/removing keys requires changing the code
#     -- TIP: use tail -f <filename>.txt to display to contents of <filename>.txt in real time (in a new terminal window)
# - python3 must be installed
# - Packages needed (I used pip to install)
#     -- pandas, matplotlib, numpy, and xlsxwriter
# - replace parameters accordingly in main function 

# TO RUN:
# Windows:
#     1. open cmd prompt
#     2. find location of python.exe using 'where python.exe'
#         -- mine is C:\Users\czhang\Desktop>C:\Users\czhang\AppData\Local\Programs\Python\Python38-32\python.exe
#     3. navigate to directory of this file using 'cd <path>'
#     4. run 'C:path\to\python.exe main.py'
# Mac:
#     1. navigate to directory of this file using 'cd <path>'
#     2. run 'python3 main.py' 


""" 
TODO:
- add benchmark data points
- keep only 1 data point per second
- make time start at 00:00.00
- get interval stats

"""

import sys
sys.path.append('.')

from top_parser import TopParser
from grapher import Grapher

def main():

    # CHANGE PARAMETERS HERE ======================================================
    # parameters: filename of your top output file, where your top output text file is saved
    tp = TopParser(filename='example-top-output', dir_text=r'/Users/cpqa/Desktop/top-graphs/') 
    # =============================================================================

    text = tp.parseText()
    data = tp.fillDict(text)
    summary = tp.getSummaryData(data)
    # print(summary)

    # CHANGE PARAMETERS HERE ======================================================
    # parameters (leave 1st and 2nd parameter): 
    #       - filename that you want your xlsx file to be, 
    #       - where you want your xlsx file to be saved
    g = Grapher(data=data, summary=summary, filename='example-top-output', dir_xlsx=r'/Users/cpqa/Desktop/top-graphs/')
    # =============================================================================

    df1, df_np = g.convertToNumpy()
    g.createPlot(df_np)
    g.saveAsXLSX(df1)

if __name__ == "__main__":
    main()