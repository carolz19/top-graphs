# DESCRIPTION:
# Converts top output in a text file into a graphical format.

# READ ME BEFORE EXECUTING:
# - Make sure to use this command: top | grep Bria\ Enterprise >> <filename>.txt 
#     -- modifying the command by adding/removing keys requires changing the code
#     -- TIP: use tail -f <filename>.txt to display to contents of <filename>.txt in real time (in a new terminal window)
# - python3 must be installed
# - Packages needed (I use pip to install)
#     -- pandas, matplotlib, numpy, and xlsxwriter
# - replace parameters accordingly in main function (at the very bottom of this file)

# TO RUN:
# Windows:
#     1. open cmd prompt
#     2. find location of python.exe using 'where python.exe'
#         -- mine is C:\Users\czhang\Desktop>C:\Users\czhang\AppData\Local\Programs\Python\Python38-32\python.exe
#     3. navigate to directory of this file using 'cd <path>'
#     4. run r'C:path\to\python.exe convert-to-csv.py'
# Mac:
#     1. navigate to directory of this file using 'cd <path>'
#     2. run r'python3 convert-to-csv.py' 


""" 
TODO:
- add benchmark data points
- keep only 1 data point per second
- make time start at 00:00.00
- get interval stats

"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Converts output from linux top command into a dictionary of time, cpu, mem, pow, and pagein values
class TopParser(object): 

    def __init__(self, filename, dir_text):
        self.filename = filename
        self.dir_text = dir_text
        self.data = {}
    
    def parseText(self) -> str:
        # Convert text file to list of rows
        text = open(self.dir_text + self.filename + '.txt', 'r')
        text = text.read().replace('M', '')
        text = text.replace('+', '')
        text = text.replace('-', '')
        text = text.split('\n')
        return text

    def fillDict(self, text) -> dict:
        # Initialize dictionary
        data = {
            'time': [],
            'cpu': [],
            'mem': [],
            'pow': [],
            'pageins': [],
        }

        # Fill dictionary
        for row in text:
            row = ' '.join(row.split()) # remove all redundant spaces
            row = row.split(' ') # create a list object

            if len(row) == 37:
                data.get('time').append(row[4])
                data.get('cpu').append(float(row[3]))
                data.get('mem').append(float(row[8]))
                data.get('pow').append(float(row[27]))
                data.get('pageins').append(float(row[25]))

        self.data = data

        return data

    def getSummaryData(self, data) -> dict:
        summary = {}

        # Get individual data points
        summary['max_cpu'] = max(data.get('cpu'))
        summary['avg_cpu'] = sum(data.get('cpu')) / len(data.get('cpu'))
        summary['max_mem'] = max(data.get('mem'))
        summary['start_mem'] = data.get('mem')[0]
        summary['end_mem'] = data.get('mem')[len(data.get('mem')) - 1]

        return summary


# Creates graph given dictionary of time, cpu, mem, pow, and pagein values
class Grapher(object):

    def __init__(self, data, filename, dir_xlsx):
        self.data = data # dictionary
        self.filename = filename # filename
        self.dir_xlsx = dir_xlsx # directory path where xlsx file will be save

    def convertToNumpy(self):
        # Create a dataframe from data
        df1 = pd.DataFrame(self.data)

        # Convert to numpy array
        df_np = pd.DataFrame(df1).to_numpy()

        return df1, df_np

    def plotData(self, axs, df_np):
        axs[0].plot(df_np[:,0], df_np[:,1], "b-", label="CPU")
        axs[1].plot(df_np[:,0], df_np[:,2], "r-", label="Memory")
        axs[2].plot(df_np[:,0], df_np[:,3], "g-", label="Power")
        axs[3].plot(df_np[:,0], df_np[:,4], "c-", label="Pageins")

    def setAxisLables(self, axs):
        axs[0].set_ylabel('CPU')
        axs[1].set_ylabel('Memory')
        axs[2].set_ylabel('Power')
        axs[3].set_ylabel('Pageins')
        axs[3].set_xlabel('Execution Time')

    def formatPlot(self, axs):
        # Adjust x-axis spacing
        xloc = plt.MaxNLocator(25)
        axs[0].xaxis.set_major_locator(xloc)

        # Formatting layout
        plt.tight_layout()

    def createPlot(self, df_np):
        # Create subplots
        fig, axs = plt.subplots(nrows=4, sharex=True, figsize=(20,12))

        self.plotData(axs, df_np)
        self.setAxisLables(axs)
        self.formatPlot(axs)

        # Save figure
        plt.savefig(fname=self.dir_xlsx + self.filename + '.jpg')
        plt.show()

    def saveAsXLSX(self, df1):
        # Storing data in a excel file
        with pd.ExcelWriter(self.dir_xlsx + self.filename + '.xlsx', engine='xlsxwriter') as writer: # pylint: disable=abstract-class-instantiated
            
            # Import DataFrame to excel file
            df1.to_excel(excel_writer=writer, sheet_name='Sheet1', startrow=73, startcol=0)

            # Get workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']

            # Add title to sheet
            cell_format = workbook.add_format({'bold':True, 'font_size': 30})
            worksheet.write_string(0,0,'Benchmark Testing Results', cell_format)

            # Insert PyPlots
            worksheet.insert_image('A2', self.dir_xlsx + self.filename + '.jpg')

def main():

    # CHANGE PARAMETERS HERE ======================================================
    # parameters: filename of your top output file, where your top output text file is saved
    tg = TopParser(filename='example-top-output', dir_text=r'/Users/cpqa/Desktop/top-graphs/') 
    # =============================================================================

    text = tg.parseText()
    data = tg.fillDict(text)
    summary = tg.getSummaryData(data)
    print(summary)

    # CHANGE PARAMETERS HERE ======================================================
    # parameters (leave first parameter): filename that you want your xlsx file to be, where you want your xlsx file to be saved
    g = Grapher(data=data, filename='example-top-output', dir_xlsx=r'/Users/cpqa/Desktop/top-graphs/')
    # =============================================================================

    df1, df_np = g.convertToNumpy()
    g.createPlot(df_np)
    g.saveAsXLSX(df1)

if __name__ == "__main__":
    main()

