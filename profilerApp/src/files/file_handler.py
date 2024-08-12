"""
This module defines the `FileHandler` class, which provides functionality for handling 
and processing flat files.

The `FileHandler` class is designed to manage file uploads, 
specifically handling CSV and Excel files. 
It includes methods to read data from these file formats, clean and process the data, 
and save it in CSV format. The class also generates and saves
metadata about the file in JSON format.

Key functionalities of `FileHandler` include:
- Uploading and processing CSV files.
- Uploading and processing Excel files.
- Cleaning and formatting data from the files.
- Saving processed data and metadata.

Dependencies:
- `json`: For handling JSON data.
- `io`: For handling in-memory file-like objects.
- `os`: For interacting with the file system.
- `pandas`: For data manipulation and file handling.
- `flask`: For accessing application configuration.

Classes:
- `FileHandler`: A handler for processing and managing flat files such as CSV and Excel.

Methods:
- `__init__(file_name: str, properties: dict)`: 
        Initializes the `FileHandler` instance with file name and properties.
- `upload_csv(file) -> None`: 
        Processes a CSV file-like object, cleans the data, saves it as a CSV file, 
        and writes properties to a JSON file.
- `upload_xlsx(file) -> None`: 
    Processes an Excel file-like object, saves it as a CSV file, 
    and writes properties to a JSON file.
"""

import json
from io import StringIO, BytesIO
import os

import pandas as pd
from flask import current_app

class FileHandler():
    """
    A class for preparing flat files and serving the profile data. 
    It reads data from a file-like object,
    processes it, and provides profiling statistics for each column.
    """
    def __init__(self, file_name:str, properties:dict):
        """
        Initializes the flatFileHandler with the given parameters.

        Parameters:
        - fileName (str): The name of the file (without extension).
        - properties (dict): Dictionary containing the file properties like separator, 
            header row, and quote character.
        """
        self.file_name = file_name
        self.properties = properties
        self.df = None

    def upload_csv(self, file) -> None:
        """
        If the file is a CSV file than the cleanCSV method data reads and cleans the file 
        and puts it into a pandas DataFrame and saves it.
        It gets processes according to the specified separator and quote character.

        Parameters:
        - file (File-like object): The file-like object containing CSV data.
        """

        quotechar = self.properties['quotechar']
        header_row = self.properties['header_row']
        delimiter = self.properties['delimiter']

        file_content =  file.read().decode('utf-8').split('\r\n')
        cleaned_lines = []
        for row in file_content:
            if row:
                if row.startswith(quotechar) and row.endswith(quotechar):   
                    row = row[1:-1]
                    row=row.replace(quotechar+quotechar,quotechar)
                cleaned_lines.append(row)
        
        cleaned_content = '\r\n'.join(cleaned_lines)

        csv_file_like = StringIO(cleaned_content)
        self.df = pd.read_csv(csv_file_like, quotechar=quotechar, delimiter=delimiter,\
                               escapechar='\\', engine='python', header=header_row)
        self.df.to_csv(os.path.join(current_app.config['csvFolder'], f"{self.file_name}.csv"),\
                        index=False)

        properties_json = json.dumps(self.properties, indent=4)
        properties_file_path = os.path.join(current_app.config['csvFolder'], \
                                            f"{self.file_name}.json")

        with open(properties_file_path, 'w', encoding='utf-8') as json_file:
            json_file.write(properties_json)

    
    def upload_xlsx(self, file) -> None:
        """
        Loads the data from an Excel file into a pandas DataFrame and saves it as csv.

        Reads the data from the Excel file, processes it, and creates a pandas DataFrame
        with the appropriate column names and data. 
        Afterwards it saves the file as CSV in the back-end.
        """
        xlsx_file = BytesIO(file.read())
        df = pd.read_excel(xlsx_file, engine='openpyxl', header=self.properties['headerRow'])
        df.to_csv(os.path.join(current_app.config['csvFolder'], f"{self.file_name}.csv"), \
                   index=False, quotechar=self.properties['quotechar'])

        properties_json = json.dumps(self.properties, indent=4)
        properties_file_path = os.path.join(current_app.config['csvFolder'], \
                                             f"{self.file_name}.json")

        with open(properties_file_path, 'w', encoding='utf-8') as json_file:
            json_file.write(properties_json)
