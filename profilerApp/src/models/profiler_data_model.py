from src import db


class ingestionOverview(db.Model):
    """
    Provides an overview of the ingestion details for a particular table and column.

    Attributes:
        table (str): Name of the table.
        column (str): Name of the column.
        table_id (int): Unique identifier for the table.
        connection_id (str): Identifier of the associated database connection.
        column_length (int): Length of the column.
        column_type (str): Data type of the column.
        data_preview (str): Preview of the first 10 elements of the column.
        median_value (float): Median value of the column.
        mean_value (float): Mean value of the column.
        min_value (float): Minimum value of the column.
        max_value (float): Maximum value of the column.
        number_nans (int): Number of NaN values in the column.
        number_unique (int): Number of unique values in the column.
        number_distinct (int): Number of distinct values in the column.
        patterns (str): Patterns found in the column.
        histogram (str): Base64-encoded histogram image of the column.
        boxplot (str): Base64-encoded boxplot image of the column.

    Methods:
        __repr__: Represents the ingestion overview instance as a string.
        
    """
    table = db.Column(db.String(80),  nullable=False)
    column = db.Column(db.String(80), nullable=False)
    table_id = db.Column(db.Integer, nullable=False)
    connection_id = db.Column(db.String(80), nullable=False)
    column_length = db.Column(db.Integer, nullable=False)
    column_type = db.Column(db.String(80), nullable=False)
    data_preview = db.Column(db.Text, nullable=True)
    median_value = db.Column(db.Float, nullable=False)
    mean_value = db.Column(db.Float, nullable=False)
    min_value = db.Column(db.Float, nullable=False)
    max_value = db.Column(db.Float, nullable=False)
    number_nans = db.Column(db.Integer, nullable=False)
    number_unique = db.Column(db.Integer, nullable=False) 
    number_distinct= db.Column(db.Integer, nullable=False)
    patterns = db.Column(db.String(80), nullable=True)
    histogram = db.Column(db.Text, nullable=True)
    boxplot = db.Column(db.Text, nullable=True)


    __table_args__ = (
        db.PrimaryKeyConstraint(
            table, column,
            ),
        )
    def __repr__(self):

        return f"Table('{self.table}', Column('{self.column}')"
