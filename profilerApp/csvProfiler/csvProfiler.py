import pandas as pd
from io import StringIO
import re

class CSVProfile():
    """
    A class for profiling CSV data. It reads CSV data from a file-like object,
    processes it, and provides profiling statistics for each column.
    """
    def __init__(self, file, separator, headerRow, quotechar):
        """
        Initializes the CSVProfiler with the given parameters.

        Parameters:
        - file (file-like object): A file-like object containing CSV data.
        - separator (str): The character used to separate values in the CSV file.
        - header_row (int): The row number (0-indexed) that contains the column names.
        - quotechar (str): The character used to quote fields in the CSV file.
        """
        self.file = file
        self.separator = separator
        self.headerRow = headerRow
        self.quotechar = quotechar
        self.df = None

    def convertToCsv(self):
        """
        Converts the CSV data from the file into a pandas DataFrame.
        
        Reads the CSV data from the provided file-like object, processes it
        according to the specified separator and quote character, and 
        creates a pandas DataFrame with the appropriate column names and data.
        """
        csvFile = StringIO(self.file.stream.read().decode("UTF-8"), newline=None)
        lines = csvFile.readlines()
        csvConvertedData = []
        pattern = rf'{self.separator}(?=(?:[^{self.quotechar}]*"[^{self.quotechar}]*{self.quotechar})*[^{self.quotechar}]*$)'
        for rowNumber, row in enumerate(lines): 
            row = row.strip('\n')
            if rowNumber == self.headerRow:
                columnNames = row.split(self.separator)  #re.split(pattern, row)
            elif rowNumber > self.headerRow:
                row = row[1:-1]
                row = row.replace(f'{self.quotechar}{self.quotechar}', self.quotechar)
                csvConvertedData.append(re.split(pattern, row))

        self.df = pd.DataFrame(csvConvertedData, columns=columnNames)

    def csvStandardProfiler(self):
        """
        Profiles the DataFrame and returns statistics for each column.
        
        If the DataFrame has not been created yet, it calls `convert_to_csv()` 
        to create it. It then calculates various statistics for each column, 
        including the number of distinct values, percentage of NaN values, 
        mean, minimum, and maximum values (where applicable).

        Returns:
        - List of dictionaries: Each dictionary contains statistics for one column
        """
        if self.df is None:
            self.convertToCsv()

        columnValues = []
        for column in self.df.columns:
            column_data = self.df[column]
            unique_values_count = len(column_data.value_counts()[column_data.value_counts() == 1].index.tolist())
            nan_percentage = column_data.isna().sum() / len(column_data) * 100
            
            column_type = str(column_data.dtype)
            if column_type in ['float64', 'int64']:
                mean_value = column_data.mean()
                min_value = column_data.min()
                max_value = column_data.max()
            else:
                mean_value = "N/A"
                min_value = column_data.min()
                max_value = column_data.max()
            
            column_dict = {
                "columnName": column,
                "columnType": column_type,
                "lenColumn": len(column_data),
                "distinctValues": column_data.nunique(),
                "uniqueValues": unique_values_count,
                "nanValues": nan_percentage,
                "meanColumn": mean_value,
                "minColumn": min_value,
                "maxColumn": max_value
            }
            columnValues.append(column_dict)
        return columnValues