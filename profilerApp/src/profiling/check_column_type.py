import pandas as pd
from .numerical_profiler import NumericalProfiler
from .text_profiler import TextProfiler

class CheckType:
    """
    Take data from the backend and checks it's type.

    Parameters:
        - data (pd.Series): The data to be checked.
        - connection_classes (dict): A dictionary that maps connection 
            types to their respective classes.
    """

    def __init__(self, data:pd.Series):
        self.data = data
        self.connection_classes = {
            'int64': NumericalProfiler,
            'float64': NumericalProfiler,
            'object': TextProfiler
        }

    def check_type(self):
        """ 
        Check the type of the data and returns the appropriate profiler class.

        Returns:
        - connection_classes['NumericalProfiler']: 
            The NumericalProfiler class if the data is numerical.
        - connection_classes['TextProfiler']:
            The TextProfiler class if the data is not numerical.
            First, the data is converted to a string type.
        """
        if self.data.dtype not in ['int64', 'float64'] or self.data.isnull().all():
            dtype = "object"
            self.data = self.data.astype(str)
        else:
            dtype = str(self.data.dtype)

        return self.connection_classes[dtype], self.data, dtype

        
    def covert_to_string(self):
        """
        Convert the data to a string type.

        Returns:
        - data.astype(str): The data converted to a string type.
        """
        return self.data.astype(str)
