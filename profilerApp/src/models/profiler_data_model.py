from src.config import SingletonDB

DB = SingletonDB.get_instance()


class IngestionOverview(DB.Model):
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
    table = DB.Column(DB.String(80), nullable=False)
    column = DB.Column(DB.String(80), nullable=False)
    table_id = DB.Column(DB.Integer, nullable=False)
    connection_id = DB.Column(DB.String(80), nullable=False)
    column_length = DB.Column(DB.Integer, nullable=False)
    column_type = DB.Column(DB.String(80), nullable=False)
    median_value = DB.Column(DB.Float, nullable=False)
    mean_value = DB.Column(DB.Float, nullable=False)
    min_value = DB.Column(DB.Float, nullable=False)
    max_value = DB.Column(DB.Float, nullable=False)
    number_nans = DB.Column(DB.Integer, nullable=False)
    number_unique = DB.Column(DB.Integer, nullable=False) 
    number_distinct = DB.Column(DB.Integer, nullable=False)
    patterns = DB.Column(DB.String(80), nullable=True)
    histogram = DB.Column(DB.Text, nullable=True)
    boxplot = DB.Column(DB.Text, nullable=True)

    __table_args__ = (
        DB.PrimaryKeyConstraint('table', 'column'),
    )
    
    def __repr__(self):
        """
        Return a string representation of the IngestionOverview instance.

        The string representation includes the table name and column name.

        Returns:
            str: A string representation of the IngestionOverview instance.
        """
        return f"IngestionOverview(table='{self.table}', column='{self.column}')"
    
    def to_dict(self):
        """
        Convert the IngestionOverview instance to a dictionary representation.

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
