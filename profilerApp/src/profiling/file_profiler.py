import os
import json

from flask import current_app 
import pandas as pd

from .patternFinder import PatternFinder
from .plot_creator import PlotCreator

class FileProfiler():

    def __init__(self, file_name:str):
        """
        Initializes the profilerGenerator with the given parameters.

        Parameters:
        - file_name (str): The name of the file (without extension).
        - properties (dict): Dictionary containing the file properties like separator, 
        header row, and quote character.
        """
        self.file_name = file_name
        self.properties = self.load_properties()
        self.df = self.load_data()

    def load_properties(self) -> dict:
        """
        Loads the properties of the file into a dictionary.

        Reads properties such as the delimiter, quote character, and header row from a JSON file.
        and returns it as a dictionary.
        """
        properties_filename = os.path.join(current_app.config['csvFolder'], \
                                            f"{self.file_name}.json")
        with open(properties_filename, 'rb') as properties:
            properties = json.load(properties)
        return properties

    def load_data(self) -> None:
        """
        Loads the CSV data from the file into a pandas DataFrame.

        Reads the CSV data from the file, processes it according to the specified 
        separator and quote character, and creates a pandas DataFrame with the 
        appropriate column names and data.
        """

        file_name = os.path.join(current_app.config['csvFolder'], f"{self.file_name}.csv")
        df = pd.read_csv(file_name, quotechar=self.properties['quotechar'], \
                         delimiter=self.properties['delimiter'],\
                              header=self.properties['header_row'])
        for column in df.columns:
            test_conversion = pd.to_numeric(df[column], errors='coerce')
            if test_conversion.notna().all():
                df[column] = test_conversion
        return df
    
    def get_columns(self) -> list:
        """
        Returns the columns in the DataFrame as a list of strings.

        If the DataFrame is not present, it should be created by calling `loadCsv()`.
        
        Returns:
        - list: List of column names.
        """
        return self.df.columns.tolist()
    
    def numerical_profiler(self, column_data,  column:str) -> dict:
        """
        Calculates the profiler overview of a column with a numerical type.

        Parameters:
        - column_data (str): The numpy array with the data of the corresponding column.
        - column (str): The name of the column to profile.

        Returns:
        - dict: A dictionary containing statistics for the specified column.
        """
        
        unique_values_count = len(column_data[column_data.duplicated(keep=False) == False])
        missing_or_empty_count = column_data.isna().sum() + (column_data == '').sum()
        nan_percentage = missing_or_empty_count / len(column_data) * 100
        data_preview = self.df.head(10)
        data_preview =  data_preview.to_html(index=False, classes=["table table-bordered", \
                                                                   "table-striped", "table-hover"])

        newPlotCreator = PlotCreator(column_data, column)
            
        column_type = str(column_data.dtype)
        median_value = round(column_data.median(), 3)
        mean_value = round(column_data.mean(), 3)
        min_value = round(column_data.min(), 3)
        max_value = round(column_data.max(), 3)
        boxplot_image = newPlotCreator.get_image("boxplot")
        column_image = newPlotCreator.get_image("histogram")

        profiler_overview = {
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
                "histogram": column_image,
                "boxplot": boxplot_image
            },
            "dataPreview": data_preview
        }
        return profiler_overview
    
    def object_profiler(self, column_data, column:str) -> dict:
        """
        Calculates the profiler overview of a column with object type.

        Parameters:
        - column_data (str): The numpy array with the data of the corresponding column.
        - column (str): The name of the column to profile.

        Returns:
        - dict: A dictionary containing statistics for the specified column.
        """
        column_data = column_data.astype(str)
        column_type = str(column_data.dtype)
        unique_values_count = len(column_data[column_data.duplicated(keep=False) == False])
        missing_or_empty_count = column_data.isna().sum() + (column_data == '').sum()
        nan_percantage = missing_or_empty_count / len(column_data) * 100

        data_preview = self.df.head(10)
        data_preview =  data_preview.to_html(index=False, classes=["table table-bordered", \
                                                                   "table-striped", "table-hover"])

        number_numeric = 0
        for item in column_data:
            if item.isnumeric():
                number_numeric += 1
        min_value = column_data.min()
        max_value = column_data.max()

        pattern_finder = PatternFinder(column_data)
        patterns = pattern_finder.find_patterns()[0:10]

        profiler_overview = {
            "columnName": column,
            "columnType": column_type,
            "lenColumn": len(column_data),
            "distinctValues": column_data.nunique(),
            "uniqueValues": unique_values_count,
            "nanValues": nan_percantage,
            'baseStats': {
                "meanColumn": "N/A",
                "medianColumn": "N/A",
                "minColumn": str(min_value),
                "maxColumn": str(max_value)

            },
            "extraInfo":{
                "numberNumeric": number_numeric,
                "patterns": patterns
            },
            "dataPreview": data_preview
        }
        return profiler_overview


    def profile_file(self, column:str) -> dict:
        """
        Profiles the DataFrame and returns statistics for the specified column.

        Parameters:
        - column (str): The name of the column to profile.

        Returns:
        - dict: A dictionary containing statistics for the specified column.
        """

        column_type = str(self.df[column].dtype)
        if column_type in ['float64', 'int64']:
            profiler_overview = self.numerical_profiler(self.df[column], column)
        elif column_type == 'object':
            profiler_overview = self.object_profiler(self.df[column], column)
        return profiler_overview
    