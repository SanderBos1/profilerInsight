import pandas as pd

class csvProfilerClass():
    def __init__(self, file):
        self.df = pd.read_csv(file)

    def csvStandardProfiler(self):
        columnValues = []
        for column in self.df.columns:
            uniqueValues = len(self.df[column].value_counts()[self.df[column].value_counts() == 1].index.tolist())
            nanValues = self.df[column].isna().sum()/len(self.df[column]) * 100
            minColumn = self.df[column].min()    
            maxColumn = self.df[column].max()

            columnDict = {
                "columnName": column,
                "columnType": str(self.df[column].dtype),
                "lenColumn": len(self.df[column]),
                "distinctValues": self.df[column].nunique(),
                "uniqueValues": uniqueValues,
                "nanValues": nanValues,
                "meanColumn": self.df[column].mean() if str(self.df[column].dtype) == 'float64' or str(self.df[column].dtype) == "int64" else "N/A",
                "minColumn": float(minColumn) if str(self.df[column].dtype) == 'float64' else str(minColumn),
                "maxColumn": float(maxColumn) if str(self.df[column].dtype) == 'float64' else str(maxColumn)  
            }
            columnValues.append(columnDict)
        return columnValues