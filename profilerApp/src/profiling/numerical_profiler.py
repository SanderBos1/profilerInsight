import math

from .base_profiler import BaseProfiler
from src.utils import PlotCreator


class NumericalProfiler(BaseProfiler):
    """
    The NumericalProfiler class, implements the BaseProfiler methods for numerical data.

    """

    def mean(self) -> float:
        mean = self.data.mean()
        if math.isnan(mean):
            return "NaN"
        return int(mean)
    
        
    def median(self):
        """
        
        Calculate the median of the data.
        
        Returns:
            - np.median(self.data): The median of the data.
        """
        median = self.data.median()
        if math.isnan(median):
            return "NaN"
        return int(median)
    
    def min(self):
        """ 
        Calculate the minimum of the data.
        
        Returns:
            - np.min(self.data): The minimum of the data.
        """
        min = self.data.min()
        if math.isnan(min):
            return "NaN"
        return int(min)
    
    def max(self):
        """
        Calculate the maximum of the data.
        
        Returns:
            - np.max(self.data): The maximum of the data.
        """
        max = self.data.max()
        if math.isnan(max):
            return "NaN"
        return int(max)

    def get_histogram(self) -> str:
        """
        Generate a histogram of the data.

        Returns:
            - histogram:  Base64-encoded histogram image of the column
        
        """
        new_plot_creator = PlotCreator(self.data, self.column)
        histogram = new_plot_creator.get_image("histogram")
        return histogram
    
    def get_boxplot(self) -> str:
        """
        Generate a boxplot of the data.

        Returns:
            - boxplot: Base64-encoded boxplot image of the column
        
        """
        new_plot_creator = PlotCreator(self.data, self.column)
        boxplot = new_plot_creator.get_image("boxplot")
        return boxplot


    def profiler_output(self) -> dict:
        """
        Collect all information of the profiler into a single dictionary.

        Returns:
            - profiler_output: A dictionary containing the profiler information
        
        """
        profiler = {
            "column": self.column,
            "column_type": self.dtype,
            "column_length": self.column_length(),
            "mean": self.mean(),
            "median": self.median(),
            "min": self.min(),
            "max": self.max(),
            "unique_values": self.unique_count(),
            "distinct_values": self.distinct_count(),
            "nan_percantage": self.nan_percantage(),
            "histogram": self.get_histogram(),	
            "boxplot": self.get_boxplot()
        }

        return profiler
