import base64

import pandas as pd
from src.profiling import NumericalProfiler

def test_mean():
    """
    Test the mean function of the numerical profiler

    Raises:
        - AssertionError: If the mean of the data is not as expected.
    """
    data = pd.Series([1, 2, 3, 4, 5])
    column = 'test'
    dtype = 'int'
    profiler = NumericalProfiler(data, column, dtype)
    assert profiler.mean() == 3.0

def test_median():
    """
    Test the median function of the numerical profiler
    
    Raises:
        - AssertionError: If the median of the data is not as expected.
    """
    data = pd.Series([1, 2, 3, 4, 5])
    column = 'test'
    dtype = 'int'
    profiler = NumericalProfiler(data, column, dtype)
    assert profiler.median() == 3.0

def test_min():
    """
    Test the min function of the numerical profiler
    
    Raises:
        - AssertionError: If the minimum of the data is not as expected.
    """
    data = pd.Series([1, 2, 3, 4, 5])
    column = 'test'
    dtype = 'int'
    profiler = NumericalProfiler(data, column, dtype)
    assert profiler.min() == 1.0

def test_max():
    """
    Test the max function of the numerical profiler

    Raises:
        - AssertionError: If the maximum of the data is not as expected.
    """
    data = pd.Series([1, 2, 3, 4, 5])
    column = 'test'
    dtype = 'int'
    profiler = NumericalProfiler(data, column, dtype)
    assert profiler.max() == 5.0

def test_unique():
    """
    Test the unique_count function of the numerical profiler

    Raises:
        - AssertionError: If the number of unique values in the data is not as expected.
    """
    data = pd.Series([1, 2, 2, 2, 5])
    column = 'test'
    dtype = 'int'
    profiler = NumericalProfiler(data, column, dtype)
    assert profiler.unique_count() == 2.0

def test_distinct():
    """
    Test the distict_count function of the numerical profiler

    Raises:
        - AssertionError: If the number of distinct values in the data is not as expected.
    """
    data = pd.Series([1, 2, 2, 2, 5])
    column = 'test'
    dtype = 'int'
    profiler = NumericalProfiler(data, column, dtype)
    assert profiler.distinct_count() == 3.0

def test_nan_percentage():
    """
    Test the nan_percentage function of the numerical profiler

    Raises:
        - AssertionError: If the percentage of NaN values in the data is not as expected.
    """
    data = pd.Series([1, 2, 2, 2, None])
    column = 'test'
    dtype = 'int'
    profiler = NumericalProfiler(data, column, dtype)
    assert profiler.nan_percantage() == 20.0

def test_histogram():
    """
    Test the get_histogram function of the numerical profiler

    Raises:
        - AssertionError: If the histogram of the data is not returned as a base64 encoded string.
    """
    data = pd.Series([1, 2, 2, 2, 5])
    column = 'test'
    dtype = 'int'
    profiler = NumericalProfiler(data, column, dtype)
    histogram =  profiler.get_histogram()
    assert base64.b64encode(base64.b64decode(histogram)) 

def test_boxplot():
    """
    Test the get_boxplot function of the numerical profiler

    Raises:
        - AssertionError: If the boxplot of the data is not returned as a base64 encoded string.
    """
    data = pd.Series([1, 2, 2, 2, 5])
    column = 'test'
    dtype = 'int'
    profiler = NumericalProfiler(data, column, dtype)
    boxplot =  profiler.get_boxplot()
    assert base64.b64encode(base64.b64decode(boxplot)) 

def test_profiler_output():
    """
    
    Test the profiler output function of the numerical profiler
    
    Raises:
    
        - AssertionError: If the profiler output does not contain the expected keys.
        
    """
    data = pd.Series([1, 2, 2, 2, 5])
    column = 'test'
    dtype = 'int'
    profiler = NumericalProfiler(data, column, dtype)
    profiler_output = profiler.profiler_output()

    expected_keys = {"column", "column_type", "column_length", "mean", "median", "min", "max", \
                     "unique_values", "distinct_values", "nan_percantage", "histogram", "boxplot"}
    assert profiler_output.keys() == expected_keys