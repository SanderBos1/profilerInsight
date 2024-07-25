import pandas as pd
from io import StringIO
import re
import csv

class csvProfilerClass():
    def __init__(self, file, seperator, header, quotechar):
        self.file = file
        self.separator = seperator
        self.header = header
        self.quotechar = quotechar

    def convertToCsv(self):



        csvFile = StringIO(self.file.stream.read().decode("UTF8"), newline=None)
        lines = csvFile.readlines()

        csvConvertedData = []
        pattern = rf'{self.separator}(?=(?:[^{self.quotechar}]*"[^{self.quotechar}]*{self.quotechar})*[^{self.quotechar}]*$)'
        for rowNumber, row in enumerate(lines): 
            row = row.strip('\n')
            if rowNumber == self.header:
                columnNames = row.split(self.separator)  #re.split(pattern, row)
            elif rowNumber > self.header:
                row = row[1:-1]
                row = row.replace('""', f'{self.quotechar}')
                csvConvertedData.append(re.split(pattern, row))

        self.df = pd.DataFrame(csvConvertedData, columns=columnNames)

    def csvStandardProfiler(self):
        self.convertToCsv()
        columnValues = []
        for column in self.df.columns:
            uniqueValues = len(self.df[column].value_counts()[self.df[column].value_counts() == 1].index.tolist())
            nanValues = self.df[column].isna().sum()/len(self.df[column]) * 100
            meanColumn = self.df[column].mean() if str(self.df[column].dtype) == 'float64' or str(self.df[column].dtype) == "int64" else "N/A"
            minColumn = float(self.df[column].min()) if str(self.df[column].dtype) == 'float64' else min(self.df[column].astype(str))  
            maxColumn = float(self.df[column].max()) if str(self.df[column].dtype) == 'float64' else max(self.df[column].astype(str))
            columnDict = {
                "columnName": column,
                "columnType": str(self.df[column].dtype),
                "lenColumn": len(self.df[column]),
                "distinctValues": self.df[column].nunique(),
                "uniqueValues": uniqueValues,
                "nanValues": nanValues,
                "meanColumn": str(meanColumn),
                "minColumn": str(minColumn),
                "maxColumn": str(maxColumn)
            }
            columnValues.append(columnDict)
        return columnValues