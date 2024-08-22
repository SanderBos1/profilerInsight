import pandas as pd

class BaseProfiler():
    """
    The base profiler, implements the basic profiler methods such as mean, median, min, max, etc.

    Attributes:
        data: The data to be profiled.
        column: The name of the column to be profiled.
        dtype: The data type of the column.
    """
    def __init__(self, data:pd.Series, column:str, dtype:str):
        self.data = data
        self.column = column
        self.dtype = dtype
    
    def column_length(self):
        """
        Calculate the length of the data.

        Returns:
            - int: The length of the data.
        """
        return len(self.data)

    def mean(self):
        """
        Calculate the mean of the data.

        Returns:
            - np.mean(self.data): The mean of the data.
        """
        return self.data.mean()
    
    def median(self):
        """
        
        Calculate the median of the data.
        
        Returns:
            - np.median(self.data): The median of the data.
        """
        return self.data.median()
    
    def min(self):
        """ 
        Calculate the minimum of the data.
        
        Returns:
            - np.min(self.data): The minimum of the data.
        """
        return self.data.min()
    
    def max(self):
        """
        Calculate the maximum of the data.
        
        Returns:
            - np.max(self.data): The maximum of the data.
        """
        return self.data.max()
    
    def nan_percantage(self):
        """
        Calculate the percentage of NaN values in the data.

        Returns:
            - Float: The percentage of NaN values in the data.
        """
        nan_count = self.data.isna().sum()
        empty_string_count = (self.data == '').sum()
        nan_string_count = (self.data == "nan").sum()

        total_missing_or_empty_count = nan_count + empty_string_count + nan_string_count

        nan_percentage = total_missing_or_empty_count / len(self.data) * 100
        return float(nan_percentage)
    
    def unique_count(self):
        """
        Count the number of unique values in the data.

        Returns:
            - int: The number of unique values in the data.
        """
        unique_values = len(self.data[self.data.duplicated(keep=False) == False])
        return unique_values

    def distinct_count(self):
        """
        Count the number of distinct values in the data.

        Returns:
            - int: The number of distinct values in the data.
        """
        distinct_count = self.data.nunique()
        return distinct_count
    
    def profiler_output(self):
        """
        Collect all information of the profiler into a single dictionary.

        Returns:
            - profiler_output: A dictionary containing the profiler information
        
        """
        raise NotImplementedError
    
