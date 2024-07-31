import pandas as pd
import json
from flask import current_app
import re
import os
from ..plotCreator import plotCreator

class CSVProfiler():
    """
    A class for profiling CSV data. It reads CSV data from a file-like object,
    processes it, and provides profiling statistics for each column.
    """
    def __init__(self, fileName:str, properties:dict):
        """
        Initializes the CSVProfiler with the given parameters.

        Parameters:
        - fileName (str): The name of the CSV file (without extension).
        - properties (dict): Dictionary containing CSV file properties like separator, header row, and quote character.
        """
        self.fileName = fileName
        self.properties = properties
        self.df = None

    def convertToCsv(self, file) -> None:
        """
        Converts the CSV data from the file into a pandas DataFrame and saves it.

        Reads the CSV data from the provided file-like object, processes it
        according to the specified separator and quote character, and 
        creates a pandas DataFrame with the appropriate column names and data.

        Parameters:
        - file (File-like object): The file-like object containing the CSV data.
        """
        csvContent = file.read().decode('utf-8')
        csvLines = csvContent.split('\r\n')
        csvConvertedData = []
        quotechar = self.properties['quotechar']
        headerRow = self.properties['headerRow']
        separator = self.properties['separator']

        pattern = re.compile(rf'''{separator}(?=(?:[^{quotechar}]*{quotechar}[^{quotechar}]*{quotechar})*[^{quotechar}]*$)''')

        for rowNumber, row in enumerate(csvLines): 
            row = row.strip()

            if row:
                if row.startswith(quotechar) and row.endswith(quotechar):   
                    row = row[1:-1]
                    row=row.replace(quotechar+quotechar,quotechar)
            
                row = pattern.split(row)

                if rowNumber == headerRow:
                    columnNames = row
                elif rowNumber > headerRow:
                    csvConvertedData.append(row)


        self.df = pd.DataFrame(csvConvertedData, columns=columnNames)
        self.df.to_csv(os.path.join(current_app.config['csvFolder'], f"{self.fileName}.csv"), index=False)

        propertiesJson = json.dumps(self.properties, indent=4)
        propertiesFilePath = os.path.join(current_app.config['csvFolder'], f"{self.fileName}.json")

        with open(propertiesFilePath, 'w') as jsonFile:
            jsonFile.write(propertiesJson)

    def loadCsv(self) -> None:
        """
        Loads the CSV data from the file into a pandas DataFrame.

        Reads the CSV data from the file, processes it according to the specified 
        separator and quote character, and creates a pandas DataFrame with the 
        appropriate column names and data.
        """
    
        fileName = os.path.join(current_app.config['csvFolder'], f"{self.fileName}.csv")
        self.df = pd.read_csv(fileName, sep=self.properties['separator'], quotechar=self.properties['quotechar'], header=self.properties['headerRow'])

    def getColumns(self) -> list:
        """
        Returns the columns in the DataFrame as a list of strings.

        If the DataFrame is not present, it should be created by calling `loadCsv()`.
        
        Returns:
        - list: List of column names.
        """
        if self.df is None:
            self.loadCsv()
        return self.df.columns.tolist()

    def csvStandardProfiler(self, column:str) -> dict:
        """
        Profiles the DataFrame and returns statistics for the specified column.

        If the DataFrame has not been created yet, it calls `convertToCsv()` 
        to create it. It then calculates various statistics for the specified column, 
        including the number of distinct values, percentage of NaN values, 
        mean, minimum, and maximum values (where applicable).

        Parameters:
        - column (str): The name of the column to profile.

        Returns:
        - dict: A dictionary containing statistics for the specified column.
        """
        if self.df is None:
            self.convertToCsv()

        column_data = self.df[column]
        unique_values_count = len(column_data[column_data.duplicated(keep=False) == False])
        nan_percentage = column_data.isna().sum() / len(column_data) * 100

        newPlotCreator = plotCreator(column_data, column)
            
        column_type = str(column_data.dtype)
        if column_type in ['float64', 'int64']:
            median_value = round(column_data.median(), 3)
            mean_value = round(column_data.mean(), 3)
            min_value = round(column_data.min(), 3)
            max_value = round(column_data.max(), 3)
            boxplotImage = newPlotCreator.getImage("boxplot")
            columnImage = newPlotCreator.getImage("histogram")

            column_dict = {
                "columnName": column,
                "columnType": column_type,
                "lenColumn": len(column_data),
                "distinctValues": column_data.nunique(),
                "uniqueValues": unique_values_count,
                "nanValues": nan_percentage,
                'baseStats': {
                    "meanColumn":str(mean_value),
                    "medianColumn": str(median_value),
                    "minColumn": str(min_value),
                    "maxColumn": str(max_value),

                },
                "numericImages": {
                    "histogram": columnImage,
                    "boxplot": boxplotImage
                }
            }
        else:
            column_data = column_data.astype(str)
            mean_value = "N/A"
            median_value = "N/A"
            min_value = column_data.min()
            max_value = column_data.max()
            column_dict = {
                "columnName": column,
                "columnType": column_type,
                "lenColumn": len(column_data),
                "distinctValues": column_data.nunique(),
                "uniqueValues": unique_values_count,
                "nanValues": nan_percentage,
                'baseStats': {
                    "meanColumn": "N/A",
                    "medianColumn": "N/A",
                    "minColumn": str(min_value),
                    "maxColumn": str(max_value)

                },
            }
        return column_dict