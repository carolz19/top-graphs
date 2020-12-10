# DESCRIPTION:
# Converts top output in a text file into a graphical format.

# READ ME BEFORE EXECUTING:
# - Make sure to use this command: top | grep Bria\ Enterprise >> <filename>.txt 
#     -- modifying the command by adding/removing keys requires changing the code
#     -- TIP: use tail -f <filename>.txt to display to contents of <filename>.txt in real time (in a new terminal window)
# - python3 must be installed
# - Packages needed (I use pip to install)
#     -- pandas, matplotlib, numpy, and xlsxwriter

# (*) Replace filename variable with your file name (don't add extension, aka .txt or .csv)
# (**) Replace directory_text with the directory of where your text file is
#     -- format: here/thenhere/finallyhere/
# (***) Replace directory_xlsx with the directory you'd like to save your csv file

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

# (*)
filename = 'example-top-output'
# (**)
# directory_text = r'C:\Users\czhang\Desktop\\' # win
directory_text = r'/Users/cpqa/Desktop/top-graphs/' # mac
# (***)
# directory_xlsx = r'C:\Users\czhang\Desktop\\' # win
directory_xlsx = r'/Users/cpqa/Desktop/top-graphs/' # mac

class TopGraphs:   
    
    def parseText(self) -> str:
        ''' Convert text file to list of rows '''
        text = open(directory_text + filename + '.txt', 'r')
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

    def convertToNumpy(self, data):
        # Create a dataframe from data
        df1 = pd.DataFrame(data)

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
        plt.savefig(fname=directory_xlsx + filename + '.jpg')
        plt.show()

    def saveAsXLSX(self, df1):
        # Storing data in a excel file
        with pd.ExcelWriter(directory_xlsx + filename + '.xlsx', engine='xlsxwriter') as writer: # pylint: disable=abstract-class-instantiated
            
            # Import DataFrame to excel file
            df1.to_excel(excel_writer=writer, sheet_name='Sheet1', startrow=73, startcol=0)

            # Get workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']

            # Add title to sheet
            cell_format = workbook.add_format({'bold':True, 'font_size': 30})
            worksheet.write_string(0,0,'Benchmark Testing Results', cell_format)

            # Insert PyPlots
            worksheet.insert_image('A2', directory_xlsx + filename + '.jpg')

def main():
    tg = TopGraphs()
    text = tg.parseText()
    data = tg.fillDict(text)
    summary = tg.getSummaryData(data)
    print(summary)

    df1, df_np = tg.convertToNumpy(data)
    tg.createPlot(df_np)
    tg.saveAsXLSX(df1)

if __name__ == "__main__":
    print('in main fn')
    main()

