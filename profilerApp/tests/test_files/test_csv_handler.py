from io import BytesIO

import pandas as pd
from pandas.testing import assert_frame_equal

from src.files import CsvHandler


def test_clean_csv():
    """
        Test the clean method of the CsvHandler class.

        Args:
            - N / A 

        Returns:
            - N / A 

        Raises:
            - AssertionError: If the cleaned data frame is not as expected.
        
    """
    csv_data = 'col1,col2\n"val1","val2"\n"val3","val4"'
    csv_file = BytesIO(csv_data.encode('utf-8'))

    properties = {'quotechar': '"', 'header_row': 0, 'delimiter': ','}

    file_handler = CsvHandler(properties)

    cleaned_df = file_handler.clean(csv_file)

    expected_df = pd.DataFrame({'col1': ['val1', 'val3'], 'col2': ['val2', 'val4']})
    assert_frame_equal(cleaned_df, expected_df)

