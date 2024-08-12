
import numpy as np
import pandas as pd
from src.config import get_database
from ..models import IngestionOverview
from .patternFinder import PatternFinder
from .plot_creator import PlotCreator

db = get_database()


class Profiler:

    """
    A class to profile data and save profiling information to a database.

    Attributes:
        data (np.ndarray): The data to be profiled.
        table_name (str): The name of the table in the database.
        column (str): The name of the column in the table.
        table_id (int): The ID of the table.
        connection_id (int): The ID of the database connection.
    """

    def __init__(self, data, table_name:str, column:str, table_id:str,  connection_id:str):

        """
        Initializes the Profiler with the specified table and column names.

        Args:
            data (np.ndarray): The data to be profiled. Must be a NumPy array.
            table_name (str): The name of the table in the database.
            column (str): The name of the column in the table.
            table_id (int): The ID of the table.
            connection_id (int): The ID of the database connection.
        """
        self.data = data
        self.table_name = table_name
        self.column = column
        self.table_id = table_id
        self.connection_id = connection_id

    def get_overview(self) -> dict:

        """
        Calculates and returns an overview of the data, including type, length, 
        number of NaNs, and number of unique values.

        Returns:
            dict: A dictionary containing the following keys:
                - "column_type": The data type of the column.
                - "column_length": The number of elements in the column.
                - "data_preview": The first 10 elements of the column.
                - "nan_count": The number of NaN values in the column.
                - "unique_count": The number of unique values in the column.
                - "mean": The mean value of the column.
                - "median": The median value of the column.
                - "min": The minimum value of the column .
                - "max": The maximum value of the column .
                - "patterns": The most common patterns in the column (if string).
                - "histogram": Base64-encoded histogram image of the column (if numeric).
                - "boxplot": Base64-encoded boxplot image of the column (if numeric
        """
        self.data = pd.Series(self.data, name=self.column)
        
        column_type = str(self.data.dtype)
        patterns   = None
        histogram  = None
        boxplot    = None

        if column_type  in ['int64', 'float64']:
            column_type = 'numeric'
            new_plot_creator = PlotCreator(self.data, self.column)
            histogram = new_plot_creator.get_image("histogram")
            boxplot = new_plot_creator.get_image("boxplot")
            mean_value = round(float(self.data.mean()), 3)
            median_value = round(float(self.data.median()), 3)
            min_value = round(float(self.data.min()), 3)
            max_value = round(float(self.data.max()), 3)

        else:
            column_type = 'string'
            self.data = self.data.astype(str)
            pattern_finder = PatternFinder(self.data)
            patterns = pattern_finder.find_patterns()[0:10]
            mean_value = self.data.mean()
            median_value = self.data.median()
            min_value = self.data.min()
            max_value =  self.data.max()

        column_length = len(self.data)
        nan_count = np.count_nonzero(np.isnan(self.data))
        distinct_count = len(np.unique(self.data))
        unique_count= len(self.data[self.data.duplicated(keep=False) == False])


        return {
            "column_type": column_type,
            "data_preview": list(self.data[:10]),
            "column_length": column_length,
            "nan_count": nan_count,
            "distinct_count": distinct_count,
            "unique_count": unique_count,
            "mean": mean_value,
            "median": median_value, 
            "min": min_value,
            "max": max_value,
            "patterns": patterns,
            "histogram": histogram,
            "boxplot": boxplot
        }


    def save_overview(self) -> None:
        """
        Saves the overview of the data to the database. If a row with the specified
        table name and column already exists, it is updated; otherwise, a new row
        is inserted.

        This method commits the changes to the database.

        """
        
        information = self.get_overview()
        ingestion_overview = IngestionOverview(
            table=self.table_name,
            column=self.column,
            table_id = self.table_id,
            connection_id = self.connection_id,
            column_length=information["column_length"],
            data_preview=information["data_preview"],
            median_value=information["median"],
            mean_value=information["mean"],
            min_value=information["min"],
            max_value=information["max"],
            number_nans=information["nan_count"],
            number_unique=information["unique_count"],
            number_distinct=information["distinct_count"],
            column_type=information["column_type"],
            patterns=information["patterns"],
            histogram=information["histogram"],
            boxplot=information["boxplot"]
        )

        db.session.merge(ingestion_overview)
        db.session.commit()
