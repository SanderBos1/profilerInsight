import pandas as pd
import json
from flask import current_app
from io import StringIO, BytesIO
import os

class FileHandler():
    """
    A class for preparing flat files and serving the profile data. It reads data from a file-like object,
    processes it, and provides profiling statistics for each column.
    """
    def __init__(self, file_name:str, properties:dict):
        """
        Initializes the flatFileHandler with the given parameters.

        Parameters:
        - fileName (str): The name of the file (without extension).
        - properties (dict): Dictionary containing the file properties like separator, header row, and quote character.
        """
        self.file_name = file_name
        self.properties = properties
        self.df = None

    def uploadCSV(self, file) -> None:
        """
        If the file is a CSV file than the cleanCSV method data reads and cleans the file and puts it into a pandas DataFrame and saves it.
        It gets processes according to the specified separator and quote character.

        Parameters:
        - file (File-like object): The file-like object containing CSV data.
        """

        quotechar = self.properties['quotechar']
        header_row = self.properties['headerRow']
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
        self.df = pd.read_csv(csv_file_like, quotechar=quotechar, delimiter=delimiter, escapechar='\\', engine='python', header=header_row)
        self.df.to_csv(os.path.join(current_app.config['csvFolder'], f"{self.file_name}.csv"), index=False)

        properties_json = json.dumps(self.properties, indent=4)
        properties_file_path = os.path.join(current_app.config['csvFolder'], f"{self.file_name}.json")

        with open(properties_file_path, 'w') as jsonFile:
            jsonFile.write(properties_json)

    
    def uploadXLSX(self, file) -> None:
        """
        Loads the data from an Excel file into a pandas DataFrame and saves it as csv.

        Reads the data from the Excel file, processes it, and creates a pandas DataFrame
        with the appropriate column names and data. Afterwards it saves the file as CSV in the back-end.
        """
        xlsx_file = BytesIO(file.read())
        df = pd.read_excel(xlsx_file, engine='openpyxl', header=self.properties['headerRow'])
        df.to_csv(os.path.join(current_app.config['csvFolder'], f"{self.file_name}.csv"), index=False, quotechar=self.properties['quotechar'])

        properties_json = json.dumps(self.properties, indent=4)
        properties_file_path = os.path.join(current_app.config['csvFolder'], f"{self.file_name}.json")

        with open(properties_file_path, 'w') as jsonFile:
            jsonFile.write(properties_json)



    
  