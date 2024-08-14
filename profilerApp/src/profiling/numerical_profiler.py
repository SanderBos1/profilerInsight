from .base_profiler import BaseProfiler
from .plot_creator import PlotCreator


class NumericalProfiler(BaseProfiler):
    """
    The NumericalProfiler class, implements the BaseProfiler methods for numerical data.

    """

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
            "mean": int(self.mean()),
            "median": int(self.median()),
            "min": int(self.min()),
            "max": int(self.max()),
            "unique_values": self.unique_count(),
            "distinct_values": self.distinct_count(),
            "nan_percantage": self.nan_percantage(),
            "histogram": self.get_histogram(),	
            "boxplot": self.get_boxplot()
        }

        return profiler
