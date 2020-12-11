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




# def main():

#     # CHANGE PARAMETERS HERE ======================================================
#     # parameters: filename of your top output file, where your top output text file is saved
#     tp = TopParser(filename='example-top-output', dir_text=r'/Users/cpqa/Desktop/top-graphs/') 
#     # =============================================================================

#     text = tp.parseText()
#     data = tp.fillDict(text)
#     summary = tp.getSummaryData(data)
#     print(summary)

#     # CHANGE PARAMETERS HERE ======================================================
#     # parameters (leave first parameter): filename that you want your xlsx file to be, where you want your xlsx file to be saved
#     g = Grapher(data=data, filename='example-top-output', dir_xlsx=r'/Users/cpqa/Desktop/top-graphs/')
#     # =============================================================================

#     df1, df_np = g.convertToNumpy()
#     g.createPlot(df_np)
#     g.saveAsXLSX(df1)

# if __name__ == "__main__":
#     main()

