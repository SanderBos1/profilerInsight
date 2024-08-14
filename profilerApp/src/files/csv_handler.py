from io import StringIO
import os

import pandas as pd
from flask import current_app

from src.files.base_handler import FileHandler


class CsvHandler(FileHandler):
    """
    A class for preparing A CSV file.
    It cleans the csv and converts it into a pandas DataFrame.
    This data frame is than saved as a CSV file and the properties are saved as a JSON file.

    Attributes:
    - properties (dict): Dictionary containing the file properties like separator, 
        header row, and quote character.
    """

    def clean(self, file) -> None:
        """
        Read the CSV file and cleans the data.

        Args:
            - N / A 

        Returns:
            DataFrame: A pandas DataFrame containing the cleaned CSV data.

        Raises:
            - N / A
        
        """
        file_content =  file.read().decode('utf-8').split('\r\n')
        cleaned_lines = []
        for row in file_content:
            if row:
                if row.startswith(self.quotechar) and row.endswith(self.quotechar):   
                    row = row[1:-1]
                    row=row.replace(self.quotechar+self.quotechar,self.quotechar)
                cleaned_lines.append(row)
        
        cleaned_content = '\r\n'.join(cleaned_lines)

        csv_file_like = StringIO(cleaned_content)
        df = pd.read_csv(csv_file_like, quotechar=self.quotechar, delimiter=self.delimiter,\
                               escapechar='\\', engine='python', header=self.header_row)
        return df

    def save(self, df, file_name) -> None:
        """
        Save the cleaned CSV file as a CSV file in the back-end.

        Args:
            - file_name (str): The name of the file to save the CSV data in.

        Returns:
            - N / A

        Raises:
            - N / A
        
        """
        save_path = os.path.join(current_app.config['csv_folder'], f"{file_name}.csv")
        df.to_csv(save_path, index=False)
