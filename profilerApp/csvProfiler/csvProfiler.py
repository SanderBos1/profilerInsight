import pandas as pd
import csv
from io import StringIO

class csvProfilerClass():
    def __init__(self, file, seperator, header, quotechar):
        self.file = file
        self.separator = seperator
        self.header = header
        self.quotechar = quotechar

    def convertToCsv(self):
        self.df = pd.read_csv(self.file, delimiter=self.separator, header=self.header, quotechar=self.quotechar)
        

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
                "meanColumn": meanColumn,
                "minColumn": minColumn,
                "maxColumn": maxColumn
            }
            columnValues.append(columnDict)
        return columnValues