from io import BytesIO

from openpyxl import Workbook
from src.files import XlsxHandler
import pandas as pd
from pandas.testing import assert_frame_equal

def test_clean_xlsx():
    """
        Test the clean method of the XlsxHandler class.

        Args:
            - N / A 

        Returns:
            - N / A 

        Raises:
            - AssertionError: If the cleaned data frame is not as expected.
        
    """
    wb = Workbook()
    ws = wb.active
    data = [
            ['col1', 'col2'],
            ['val1', 'val2'],
            ['val3', 'val4']
        ]

    for row in data:
        ws.append(row)

    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)

    properties = {'quotechar': '"', 'header_row': 0, 'delimiter': ','}

    xlsx_handler = XlsxHandler(properties)

    cleaned_df = xlsx_handler.clean(xlsx_file)

    expected_df = pd.DataFrame({'col1': ['val1', 'val3'], 'col2': ['val2', 'val4']})
    assert_frame_equal(cleaned_df, expected_df)

