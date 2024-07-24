import pandas as pd
import csv

class csvProfilerClass():
    def __init__(self, file, seperator, header, quotechar):
        self.file = file
        self.separator = seperator
        self.header = header
        self.quotechar = quotechar

    def convertToCsv(self):
        csvConverted = []
        for line in self.file:
            decodedLine = line.decode('utf-8')
            cleanedDecodedLine = decodedLine.replace("\r", "").replace("\n", "").replace('"', '')
            csvConverted.append(cleanedDecodedLine)

        csv_file = 'cleaned.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=self.separator, quotechar=self.quotechar, escapechar='\\')
            for line in csvConverted:
                writer.writerow([line])

        self.df = pd.read_csv(csv_file, delimiter=self.separator, header=self.header, quotechar=self.quotechar, quoting=csv.QUOTE_NONE, on_bad_lines="skip",  index_col=False)
     

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