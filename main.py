""" 
TODO:
- keep only 1 data point per second (?)
- make time start at 00:00.00
- get interval stats

"""

import sys
sys.path.append('.')

from top_parser import TopParser
from grapher import Grapher

def main():

    # parameters: filename of your top output file, where your top output text file is saved
    tp = TopParser(filename=str(sys.argv[0]), dir_text=str(sys.argv[1])) 

    text = tp.parseText()
    data = tp.fillDict(text)
    summary = tp.getSummaryData(data)

    # parameters (leave data and summary parameter): 
    #       - filename that you want your xlsx file to be, 
    #       - where you want your xlsx file to be saved
    g = Grapher(data=data, summary=summary, filename=str(sys.argv[0]), dir_xlsx=str(sys.argv[1]))

    df1, df_np = g.convertToNumpy()
    g.createPlot(df_np)
    g.saveAsXLSX(df1)

if __name__ == "__main__":
    main()
