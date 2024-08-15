from .base_profiler import BaseProfiler
from src.utils import PatternFinder

class TextProfiler(BaseProfiler):
    """
    The TextProfiler class, implements the BaseProfiler methods 
    for mixed data and data with only strings.

    """
    def get_patterns(self) -> list:
        """
        Find patterns in data.

        Returns:
            - patterns: A list of patterns found in the data.
        
        """
        pattern_finder = PatternFinder()
        patterns = pattern_finder.find_patterns(self.data)[0:10]
        return patterns
    

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
            "mean": "N/A",
            "median": "N/A",
            "min": self.min(),
            "max": self.max(),
            "unique_values": self.unique_count(),
            "distinct_values": self.distinct_count(),
            "nan_percantage": self.nan_percantage(),
            "patterns": self.get_patterns()
        }

        return profiler
