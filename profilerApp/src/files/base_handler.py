import json
import os

from flask import current_app

class FileHandler():
    """
    A super class that defines the basic structure of a file handler.

    Attributes:
    - file (Object): A file-like object containing the CSV data.
    - properties (dict): Dictionary containing the file properties like separator, 
        header row, and quote character.
    """
    def __init__(self, properties:dict):
        """
        Initialize the CsvHandler with the given parameters.

        Parameters:
        - file (Object): A file-like object containing the CSV data.
        - properties (dict): Dictionary containing the file properties like separator, 
            header row, and quote character.
        """
        self.properties = properties
        self.quotechar = self.properties['quotechar']
        self.header_row = self.properties['header_row']
        self.delimiter = self.properties['delimiter']

    def clean(self, file) -> None:
        """
        Read the file and cleans the data

        Args:
            - N / A 

        Returns:
            DataFrame: A pandas DataFrame containing the cleaned CSV data.

        Raises:
            - N / A
        
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def save_properties(self, file_name) -> None:
        """
        Save the properties of the csv file in a json file using the given file name.

        Args:
            - file_name (str): The name of the file to save the properties in.

        Returns:
            - N / A

        Raises:
            - N / A
        """

        properties_json = json.dumps(self.properties, indent=4)
        properties_file_path = os.path.join(current_app.config['csv_folder'], \
                                            f"{file_name}.json")

        with open(properties_file_path, 'w', encoding='utf-8') as json_file:
            json_file.write(properties_json)
    
    def save(self, df,  file_name) -> None:  
        """
        Save the cleaned file as a CSV file in the back-end.

        Args:
            - file_name (str): The name of the file to save the CSV data in.

        Returns:
            - N / A

        Raises:
            - N / A
        
        """
        raise NotImplementedError("This method should be overridden by subclasses")
