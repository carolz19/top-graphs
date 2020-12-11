import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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