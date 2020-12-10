# """ 
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
# (***) Replace directory_csv with the directory you'd like to save your csv file

# TO RUN:
# Windows:
#     1. open cmd prompt
#     2. find location of python.exe using 'where python.exe'
#         -- mine is C:\Users\czhang\Desktop>C:\Users\czhang\AppData\Local\Programs\Python\Python38-32\python.exe
#     3. navigate to directory of this file using 'cd <path>'
#     4. run 'C:path\to\python.exe convert-to-csv.py'
# Mac:
#     1. navigate to directory of this file using 'cd <path>'
#     2. run 'python3 convert-to-csv.py'

# """

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# (*)
filename = 'm1_6.3.0RC13_OpenCloseWindows_Screenshare'
# (**)
directory_text = r'C:\Users\czhang\Desktop\\'
# (***)
directory_csv = r'C:\Users\czhang\Desktop\\'


# Convert text file to list of rows
text = open(directory_text + filename + '.txt', 'r')
text = text.read().replace('M', '')
text = text.replace('+', '')
text = text.replace('-', '')
text = text.split('\n')

# Initialize dictionary
stats = {
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
        stats.get('time').append(row[4])
        stats.get('cpu').append(float(row[3]))
        stats.get('mem').append(float(row[8]))
        stats.get('pow').append(float(row[27]))
        stats.get('pageins').append(float(row[25]))


# Create a dataframe from stats
df1 = pd.DataFrame(stats)

# Convert to numpy array
df_np = pd.DataFrame(df1).to_numpy()

# Create subplots
fig, axs = plt.subplots(nrows=4, sharex=True, figsize=(20,12))

# Plot data
axs[0].plot(df_np[:,0], df_np[:,1], "b-", label="CPU")
axs[1].plot(df_np[:,0], df_np[:,2], "r-", label="Memory")
axs[2].plot(df_np[:,0], df_np[:,3], "g-", label="Power")
axs[3].plot(df_np[:,0], df_np[:,4], "c-", label="Pageins")

# Set axis lables
axs[0].set_ylabel('CPU')
axs[1].set_ylabel('Memory')
axs[2].set_ylabel('Power')
axs[3].set_ylabel('Pageins')
axs[3].set_xlabel('Execution Time')

# Adjust x-axis spacing
xloc = plt.MaxNLocator(25)
axs[0].xaxis.set_major_locator(xloc)

# Formatting layout
plt.tight_layout()

# Save figure
# plt.title('Benchmark Testing Results')
plt.savefig(fname=filename + '.jpg')
plt.show()

# Storing data in a excel file
with pd.ExcelWriter(filename + '.xlsx', engine='xlsxwriter') as writer: # pylint: disable=abstract-class-instantiated
    
    # Import DataFrame to excel file
    df1.to_excel(excel_writer=writer, sheet_name='Sheet1', startrow=73, startcol=0)

    # Get workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # Add title to sheet
    cell_format = workbook.add_format({'bold':True, 'font_size': 30})
    worksheet.write_string(0,0,'Benchmark Testing Results', cell_format)

    # Insert PyPlots
    worksheet.insert_image('A2', filename + '.jpg')
