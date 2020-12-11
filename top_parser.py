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
        summary['Max CPU (%)'] = max(data.get('cpu'))
        summary['Avg CPU (%)'] = sum(data.get('cpu')) / len(data.get('cpu'))
        summary['Max Mem (MB)'] = max(data.get('mem'))
        summary['Start Mem (MB)'] = data.get('mem')[0]
        summary['End Mem (MB)'] = data.get('mem')[len(data.get('mem')) - 1]

        return summary