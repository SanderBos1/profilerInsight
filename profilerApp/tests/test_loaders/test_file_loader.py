import pandas as pd

from src.loaders import FileLoader


DATA = pd.DataFrame({
    'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Name': [
        'John Doe', 'Jane Smith', 'Emily Johnson', 'Michael Brown',
        'Lisa Davis', 'David Wilson', 'Alice Miller', 'Chris Moore',
        'Patricia Taylor', 'James Anderson'
    ],
    'Age': [28, 34, 45, 23, 31, 29, 41, 37, 50, 26],
    'Email': [
        'john.doe@example.com', 'jane.smith@example.com', 'emily.johnson@example.com',
        'michael.brown@example.com', 'lisa.davis@example.com', 'david.wilson@example.com',
        'alice.miller@example.com', 'chris.moore@example.com', 'patricia.taylor@example.com',
        'james.anderson@example.com'
    ]
})

def test_load_data(app):
    with app.app_context():
        file_loader = FileLoader("test_data.csv")
        df_expected = file_loader.load_data()
        pd.testing.assert_frame_equal(df_expected, DATA)

def test_load_examples(app):
    with app.app_context():
        file_loader = FileLoader("test_data.csv")
        df_expected = file_loader.load_examples()
        assert df_expected == DATA.head(10).to_html(index=False, classes=["table table-bordered", \
                                                                   "table-striped", "table-hover"])

def test_load(app):
    with app.app_context():
        file_loader = FileLoader("test_data.csv")
        column = "Name"
        column_data_expected = file_loader.load(column)
        pd.testing.assert_series_equal(column_data_expected, DATA[column])

def test_load_columns(app):
    with app.app_context():
        file_loader = FileLoader("test_data.csv")
        columns = ["ID", "Name", "Age", "Email"]
        columns_data_expected = file_loader.load_columns()
        assert columns == columns_data_expected

def test_load_properties(app):
    with app.app_context():
        file_loader = FileLoader("test_data.csv")
        properties = file_loader.load_properties()
        assert properties == {
            'header_row': 0,
            'delimiter': ',',
            'quotechar': '"'
        }
