"""
This module defines the `IngestionOverview` model for storing and managing ingestion details
of specific tables and columns.

The `IngestionOverview` class is an SQLAlchemy model that provides a structure for recording
detailed statistics and information about the columns of tables after ingestion.

Dependencies:
- `get_database`: A function to retrieve the SQLAlchemy database instance.

Classes:
- `IngestionOverview`: SQLAlchemy model class for ingestion details of a table column.

Attributes:
- `table`: Name of the table.
- `column`: Name of the column.
- `table_id`: Unique identifier for the table.
- `connection_id`: Identifier of the associated database connection.
- `column_length`: Length of the column.
- `column_type`: Data type of the column.
- `data_preview`: Preview of the first 10 elements of the column.
- `median_value`: Median value of the column.
- `mean_value`: Mean value of the column.
- `min_value`: Minimum value of the column.
- `max_value`: Maximum value of the column.
- `number_nans`: Number of NaN values in the column.
- `number_unique`: Number of unique values in the column.
- `number_distinct`: Number of distinct values in the column.
- `patterns`: Patterns found in the column.
- `histogram`: Base64-encoded histogram image of the column.
- `boxplot`: Base64-encoded boxplot image of the column.

Methods:
- `__repr__()`: Represents the ingestion overview instance as a string.
- `to_dict()`: Converts the model instance to a dictionary representation.
"""

from src.config import get_database

db = get_database()

class IngestionOverview(db.Model):
    """
    Provides an overview of the ingestion details for a particular table and column.

    This class is an SQLAlchemy model that defines the schema for storing detailed information
    and statistics about columns in tables after data ingestion.

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
        to_dict: Converts the model instance to a dictionary.
    """
    table = db.Column(db.String(80), nullable=False)
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
    number_distinct = db.Column(db.Integer, nullable=False)
    patterns = db.Column(db.String(80), nullable=True)
    histogram = db.Column(db.Text, nullable=True)
    boxplot = db.Column(db.Text, nullable=True)

    __table_args__ = (
        db.PrimaryKeyConstraint('table', 'column'),
    )
    
    def __repr__(self):
        """
        Returns a string representation of the IngestionOverview instance.

        The string representation includes the table name and column name.

        Returns:
            str: A string representation of the IngestionOverview instance.
        """
        return f"IngestionOverview(table='{self.table}', column='{self.column}')"
    
    def to_dict(self):
        """
        Converts the IngestionOverview instance to a dictionary representation.

        The dictionary includes all attributes of the instance.

        Returns:
            dict: A dictionary representation of the IngestionOverview instance.
        """
        ingestion_overview_dict = {
            "table": self.table,
            "column": self.column,
            "table_id": self.table_id,
            "connection_id": self.connection_id,
            "column_length": self.column_length,
            "column_type": self.column_type,
            "data_preview": self.data_preview,
            "median_value": self.median_value,
            "mean_value": self.mean_value,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "number_nans": self.number_nans,
            "number_unique": self.number_unique,
            "number_distinct": self.number_distinct,
            "patterns": self.patterns,
            "histogram": self.histogram,
            "boxplot": self.boxplot
        }
        return ingestion_overview_dict
