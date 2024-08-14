from io import BytesIO
import os

import pandas as pd
from flask import current_app

from src.files.base_handler import FileHandler

class XlsxHandler(FileHandler):
    """
    A class for preparing A XLSX file.
    It cleans the XLSX and converts it into a pandas DataFrame.
    This data frame is than saved as a XLSX file and the properties are saved as a JSON file.

    Attributes:
    - file (Object): A file-like object containing the XLSX data.
    - properties (dict): Dictionary containing the file properties like separator, 
        header row, and quote character.
    """

    def clean(self, file) -> object:
        """
        Read the XLSX file and cleans the data.

        Args:
            - N / A 

        Returns:
            DataFrame: A pandas DataFrame containing the cleaned CSV data.

        Raises:
            - N / A
        
        """
        xlsx_file = BytesIO(file.read())
        df = pd.read_excel(xlsx_file, engine='openpyxl', header=self.header_row)
        return df

   
    def save(self, df, file_name) -> None:
        """
        Save the cleaned XLSX file as a CSV file in the back-end.

        Args:
            - file_name (str): The name of the file to save the CSV data in.

        Returns:
            - N / A

        Raises:
            - N / A
        
        """
        save_path = os.path.join(current_app.config['csv_folder'], f"{file_name}.csv")
        df.to_csv(save_path, index=False, quotechar=self.properties['quotechar'])
