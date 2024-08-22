import json
import os


from werkzeug.utils import secure_filename
from flask import current_app

class FileSaver():
    def __init__(self, file, properties):
        self.file = file
        self.file_name = secure_filename(file.filename)
        self.properties = properties
        
    def save_file(self):
        file_path = os.path.join(current_app.config['file_folder'], self.file_name)
        self.file.save(file_path)

    def save_properties(self) -> None:
        """
        Save the properties of the csv file in a json file using the given file name.

        Args:
            - file_name (str): The name of the file to save the properties in.

        Returns:
            - N / A

        Raises:
            - N / A
        """
        file_name = self.file_name.split('.')[0]
        properties_json = json.dumps(self.properties, indent=4)
        properties_file_path = os.path.join(current_app.config['properties_folder'], \
                                            f"{file_name}.json")

        with open(properties_file_path, 'w', encoding='utf-8') as json_file:
            json_file.write(properties_json)
