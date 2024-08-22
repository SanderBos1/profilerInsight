import os
import json

import pandas as pd
from flask import current_app 

from .basic_loader import BasicLoader

class FileLoader(BasicLoader):
    """
    A class that loads data from a database into a pandas DataFrame.

    Attributes:
        - BasicLoader (class): The parent class that defines the structure of a loader class.

    """
    def __init__(self, file_name):
        """ 
        Initializes the FileLoader with the given parameters.
        
        Parameters:
            -  column (str): The name of the column to be loaded.
            - file_name (str): The name of the file (without extension).
            - properties (dict): Dictionary containing the file properties like separator,  
              header row, and quote character.
        
        
        """
        super().__init__()
        self.file_name = file_name
        self.properties= self.load_properties()

    def load_data(self) -> pd.DataFrame:
        """
        Load the data from a csv file into a pandas DataFrame.

        Returns:
        - df: A pandas DataFrame containing the data of the csv file.
        """
        file_name = os.path.join(current_app.config['file_folder'], f"{self.file_name}" )
        if file_name.split('.')[1] == 'csv':
            df = pd.read_csv(file_name, index_col=0, header=self.properties['header_row'],  
                            quotechar=self.properties['quotechar'], \
                                delimiter=self.properties['delimiter'], engine="python")
        else:
            df = pd.read_excel(file_name, index_col=0, header=self.properties['header_row'], engine="openpyxl")
        return df

    def load(self, column) -> pd.DataFrame:
        """
        Load the data from a csv file into a pandas series.

        Returns:
        - column_data: A pandas series containing the data of the specified column.
        """
        df = self.load_data()
        column_data = df.loc[:, column]
        return column_data
    
    def load_examples(self) -> pd.DataFrame:
        """
        Load the first 10 rows of the csv file into a dataframe.

        Returns:
        - df: a DataFrame containing the first 10 rows of the csv file converted to html
        """
        df = self.load_data()

        for column in df.columns:
            test_conversion = pd.to_numeric(df[column], errors='coerce')
            if test_conversion.notna().all():
                df[column] = test_conversion

        data_preview = df.head(10)
        data_preview =  data_preview.to_html(index=False, classes=["table table-bordered", \
                                                                   "table-striped", "table-hover"])
        return data_preview

    def load_columns(self):
        """
        Load the columns of the csv file into a list.

        Returns:
            - list: A list containing the column names of the csv file.
        """
        df = self.load_data()
        return df.columns.tolist()
    
    def load_properties(self) -> dict:
        """
        Loads the properties of the file into a dictionary.

        Reads properties such as the delimiter, quote character, and header row from a JSON file.
       
        Returns:
            - dict: A dictionary containing the properties of the file.
        """
        file_name = self.file_name.split('.')[0]
        properties_filename = os.path.join(current_app.config['properties_folder'], \
                                            f"{file_name}.json")
        with open(properties_filename, 'rb') as properties:
            properties = json.load(properties)
        
        return properties
