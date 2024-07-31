import pandas as pd
import json
from flask import current_app
import re
import os
from ..plotCreator import plotCreator
import csv

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

        quotechar = self.properties['quotechar']
        headerRow = self.properties['headerRow']
        delimiter = self.properties['delimiter']

        csvLines = file.split('\r\n')
        cleanedLines = []
        for row in csvLines:
            if row:
                if row.startswith(quotechar) and row.endswith(quotechar):   
                    row = row[1:-1]
                    row=row.replace(quotechar+quotechar,quotechar)
                cleanedLines.append(row)
        data = []
        csvReader = csv.reader(cleanedLines, quotechar=quotechar, delimiter=delimiter, escapechar='\\')
        for row in csvReader:
            data.append(row)

        self.df = pd.DataFrame(columns=data[headerRow], data=data[headerRow+1:])
        self.df.to_csv(os.path.join(current_app.config['csvFolder'], f"{self.fileName}.csv"), index=False)

        propertiesJson = json.dumps(self.properties, indent=4)
        propertiesFilePath = os.path.join(current_app.config['csvFolder'], f"{self.fileName}.json")

        with open(propertiesFilePath, 'w') as jsonFile:
            jsonFile.write(propertiesJson)

    def loadCSV(self) -> None:
        """
        Loads the CSV data from the file into a pandas DataFrame.

        Reads the CSV data from the file, processes it according to the specified 
        separator and quote character, and creates a pandas DataFrame with the 
        appropriate column names and data.
        """

        fileName = os.path.join(current_app.config['csvFolder'], f"{self.fileName}.csv")
        data=[]
        with open(fileName, mode='r', encoding='utf-8') as file:
            csvReader = csv.reader(file, quotechar=self.properties['quotechar'], delimiter=self.properties['delimiter'], escapechar='\\')

            for row in csvReader:
                    data.append(row)
    
        df = pd.DataFrame(columns=data[self.properties['headerRow']], data=data[self.properties['headerRow']+1:])
        for column in df.columns:
            test_conversion = pd.to_numeric(df[column], errors='coerce')
            if test_conversion.notna().any():
                df[column] = test_conversion
        self.df = df

    def getColumns(self) -> list:
        """
        Returns the columns in the DataFrame as a list of strings.

        If the DataFrame is not present, it should be created by calling `loadCsv()`.
        
        Returns:
        - list: List of column names.
        """
        if self.df is None:
            self.loadCSV()
        return self.df.columns.tolist()
    
    def csvNumericalProfiler(self, columnData,  column:str) -> dict:
        """
        Calculates the profiler overview of a column with a numerical type.

        Parameters:
        - columnData (str): The numpy array with the data of the corresponding column.
        - column (str): The name of the column to profile.

        Returns:
        - dict: A dictionary containing statistics for the specified column.
        """
        
        unique_values_count = len(columnData[columnData.duplicated(keep=False) == False])
        nan_percentage = columnData.isna().sum() / len(columnData) * 100

        newPlotCreator = plotCreator(columnData, column)
            
        column_type = str(columnData.dtype)
        median_value = round(columnData.median(), 3)
        mean_value = round(columnData.mean(), 3)
        min_value = round(columnData.min(), 3)
        max_value = round(columnData.max(), 3)
        boxplotImage = newPlotCreator.getImage("boxplot")
        columnImage = newPlotCreator.getImage("histogram")

        profilerOverview = {
            "columnName": column,
            "columnType": column_type,
            "lenColumn": len(columnData),
            "distinctValues": columnData.nunique(),
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
        return profilerOverview
    
    def csvObjectProfiler(self, columnData, column:str) -> dict:
        """
        Calculates the profiler overview of a column with object type.

        Parameters:
        - columnData (str): The numpy array with the data of the corresponding column.
        - column (str): The name of the column to profile.

        Returns:
        - dict: A dictionary containing statistics for the specified column.
        """
        columnData = columnData.astype(str)
        column_type = str(columnData.dtype)
        unique_values_count = len(columnData[columnData.duplicated(keep=False) == False])
        nan_percentage = columnData.isna().sum() / len(columnData) * 100

        numberNumeric = 0
        for item in columnData:
            if item.isnumeric():
                numberNumeric += 1
        min_value = columnData.min()
        max_value = columnData.max()
        
        profilerOverview = {
            "columnName": column,
            "columnType": column_type,
            "lenColumn": len(columnData),
            "distinctValues": columnData.nunique(),
            "uniqueValues": unique_values_count,
            "nanValues": nan_percentage,
            'baseStats': {
                "meanColumn": "N/A",
                "medianColumn": "N/A",
                "minColumn": str(min_value),
                "maxColumn": str(max_value)

            },
            "extaInfoObject":{
                "numberNumeric": numberNumeric
            }
        }
        return profilerOverview


    def csvProfiler(self, column:str) -> dict:
        """
        Profiles the DataFrame and returns statistics for the specified column.

        If the DataFrame has not been created yet, it calls `loadCSV()` 
        to create it. It then prepares a data profiler overview so that it can be sent to the frontend.
        Which overview it creates depends on the type of the column.

        Parameters:
        - column (str): The name of the column to profile.

        Returns:
        - dict: A dictionary containing statistics for the specified column.
        """
        if self.df is None:
            self.loadCSV()

        column_type = str(self.df[column].dtype)
        if column_type in ['float64', 'int64']:
            profilerOverview = self.csvNumericalProfiler(self.df[column], column)
        elif column_type == 'object':
            profilerOverview = self.csvObjectProfiler(self.df[column], column)
        return profilerOverview