import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter

# Creates graph given dictionary of time, cpu, mem, pow, and pagein values
class Grapher(object):

    def __init__(self, data, summary, filename, dir_xlsx):
        self.data = data # dictionary
        self.filename = filename # filename
        self.dir_xlsx = dir_xlsx # directory path where xlsx file will be save
        self.summary = summary # summary data (max cpu, max memory, etc)

    def convertToNumpy(self):
        # Create a dataframe from data
        df_all = pd.DataFrame(self.data)

        # Convert to numpy array
        np_all = pd.DataFrame(df_all).to_numpy()

        return df_all, np_all

    def plotData(self, axs, np_all):
        axs[0].plot(np_all[:,0], np_all[:,1], "b-", label="CPU")
        axs[1].plot(np_all[:,0], np_all[:,2], "r-", label="Memory")
        axs[2].plot(np_all[:,0], np_all[:,3], "g-", label="Power")
        axs[3].plot(np_all[:,0], np_all[:,4], "c-", label="Pageins")

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

    def createPlot(self, np_all):
        # Create subplots
        fig, axs = plt.subplots(nrows=4, sharex=True, figsize=(20,12))

        self.plotData(axs, np_all)
        self.setAxisLables(axs)
        self.formatPlot(axs)

        # Save figure
        plt.savefig(fname=self.dir_xlsx + self.filename + '.jpg')
        plt.show()

    def saveAsXLSX(self, df_all):
        ''' Storing data in a excel file '''

        # Create workbook and worksheet
        workbook = xlsxwriter.Workbook(self.dir_xlsx + self.filename + '.xlsx')
        worksheet = workbook.add_worksheet()

        # Set top row and left-most column to a smaller width
        worksheet.set_row(0, 6)
        worksheet.set_column('A:A', 1)

        # Add title
        cell_format = workbook.add_format(
            {
                'bold': True,
                'font_size': 30
            }
        )
        worksheet.write_string('B2','Benchmark Testing Results', cell_format)

        # Add summary table
        data = [list(self.summary.values())]
        worksheet.set_column('B:F', 20)
        worksheet.add_table(
            'B3:F4', 
            {
                'data': data,
                'columns': [ {'header': heading} for heading in self.summary.keys() ],
                'autofilter': False
            }
        )

        # Add PyPlot graph image
        worksheet.insert_image(
            'B6', self.dir_xlsx + self.filename + '.jpg', 
            {
                'x_scale': 0.75,
                'y_scale': 0.75
            }
        )

        workbook.close()

        # with pd.ExcelWriter(self.dir_xlsx + self.filename + '.xlsx', engine='xlsxwriter') as writer: # pylint: disable=abstract-class-instantiated
            
        #     # Import DataFrame of all data points in data dictionary to excel file
        #     df_all.to_excel(excel_writer=writer, sheet_name='Sheet1', startrow=73, startcol=1)

        #     # Get workbook and worksheet objects
        #     workbook = writer.book
        #     worksheet = writer.sheets['Sheet1']

        #     # Add title to sheet
        #     cell_format = workbook.add_format({'bold':True, 'font_size': 30})
        #     worksheet.write_string(0,1,'Benchmark Testing Results', cell_format)

        #     # TODO: summary table causes xlsx file to be corrupt
        #     # Insert summary table
        #     worksheet.add_table('B2:F3')
        #     worksheet.write_row('B2', self.summary.keys())
        #     worksheet.write_row('B3', self.summary.values())

        #     # Insert PyPlots image
        #     worksheet.insert_image('B6', self.dir_xlsx + self.filename + '.jpg')