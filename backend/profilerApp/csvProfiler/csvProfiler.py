import pandas as pd
import json
from flask import current_app
from io import StringIO
import os
from ..patternFinder import patternFinder
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

        fileContent =  file.read().decode('utf-8').split('\r\n')
        cleanedLines = []
        for row in fileContent:
            if row:
                if row.startswith(quotechar) and row.endswith(quotechar):   
                    row = row[1:-1]
                    row=row.replace(quotechar+quotechar,quotechar)
                cleanedLines.append(row)
        
        cleaned_content = '\r\n'.join(cleanedLines)

        csv_file_like = StringIO(cleaned_content)
        self.df = pd.read_csv(csv_file_like, quotechar=quotechar, delimiter=delimiter, escapechar='\\', engine='python', header=headerRow)
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
            csvReader = csv.reader(file, quotechar=self.properties['quotechar'], delimiter=self.properties['delimiter'])

            for row in csvReader:
                    data.append(row)
    
        df = pd.DataFrame(columns=data[self.properties['headerRow']], data=data[self.properties['headerRow']+1:], dtype=str)
        for column in df.columns:
            test_conversion = pd.to_numeric(df[column], errors='coerce')
            if test_conversion.notna().all():
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
        missing_or_empty_count = columnData.isna().sum() + (columnData == '').sum()
        nan_percentage = missing_or_empty_count / len(columnData) * 100
        dataPReview = self.df.head(10)
        dataPreview =  dataPReview.to_html(index=False, classes=["table table-bordered", "table-striped", "table-hover"])

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
            },
            "dataPreview": dataPreview
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
        missing_or_empty_count = columnData.isna().sum() + (columnData == '').sum()
        nanPercentage = missing_or_empty_count / len(columnData) * 100

        dataPReview = self.df.head(10)
        dataPreview =  dataPReview.to_html(index=False, classes=["table table-bordered", "table-striped", "table-hover"])

        numberNumeric = 0
        for item in columnData:
            if item.isnumeric():
                numberNumeric += 1
        min_value = columnData.min()
        max_value = columnData.max()

        newPatternFinder = patternFinder(columnData)
        patterns = newPatternFinder.find_patterns()[0:10]

        profilerOverview = {
            "columnName": column,
            "columnType": column_type,
            "lenColumn": len(columnData),
            "distinctValues": columnData.nunique(),
            "uniqueValues": unique_values_count,
            "nanValues": nanPercentage,
            'baseStats': {
                "meanColumn": "N/A",
                "medianColumn": "N/A",
                "minColumn": str(min_value),
                "maxColumn": str(max_value)

            },
            "extraInfo":{
                "numberNumeric": numberNumeric,
                "patterns": patterns
            },
            "dataPreview": dataPreview
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