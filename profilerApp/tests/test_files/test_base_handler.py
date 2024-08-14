import json

from unittest.mock import patch, mock_open

from src.files import FileHandler

@patch('builtins.open', new_callable=mock_open)
@patch('os.path.join', return_value='/mock/path/test_properties.json')
def test_save_properties_csv(mock_join, mock_open, app):
    """
        Test the save_properties method of the CsvHandler class.

        Args:
            - N / A 

        Returns:
            - N / A 

        Raises:
            - AssertionError: If the properties are not saved as expected.
        
    """    
    with app.app_context():
        properties = {'quotechar': '"', 'header_row': 0, 'delimiter': ','}
        file_name = 'test_properties'

        csv_handler = FileHandler(properties)
        csv_handler.save_properties(file_name)

        expected_properties_json = json.dumps(properties, indent=4)
        mock_open.assert_called_once_with('/mock/path/test_properties.json', 'w', encoding='utf-8')
        mock_open().write.assert_called_once_with(expected_properties_json)

