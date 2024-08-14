import pandas as pd
from src.profiling import TextProfiler

def test_min():
    """
    Test the min function of the test profiler
    
    Raises:
        - AssertionError: If the minimum of the data is not as expected.
    """
    data = pd.Series(["test", "good", "bad", "test", "good"])
    column = 'test'
    dtype = 'object'
    profiler = TextProfiler(data, column, dtype)
    assert profiler.min() == "bad"

def test_max():
    """
    Test the max function of the test profiler

    Raises:
        - AssertionError: If the maximum of the data is not as expected.
    """
    data = pd.Series(["test", "good", "bad", "test", "good"])
    column = 'test'
    dtype = 'object'
    profiler = TextProfiler(data, column, dtype)
    assert profiler.max() == "test"

def test_unique():
    """
    Test the unique_count function of the test profiler

    Raises:
        - AssertionError: If the number of unique values in the data is not as expected.
    """
    data = pd.Series(["test", "good", "bad", "test", "good"])
    column = 'test'
    dtype = 'object'
    profiler = TextProfiler(data, column, dtype)
    assert profiler.unique_count() == 1

def test_distinct():
    """
    Test the distict_count function of the test profiler

    Raises:
        - AssertionError: If the number of distinct values in the data is not as expected.
    """
    data = pd.Series(["test", "good", "bad", "test", "good"])
    column = 'test'
    dtype = 'object'
    profiler = TextProfiler(data, column, dtype)
    assert profiler.distinct_count() == 3.0

def test_nan_percentage():
    """
    Test the nan_percentage function of the test profiler

    Raises:
        - AssertionError: If the percentage of NaN values in the data is not as expected.
    """
    data = pd.Series(["test", "good", "bad", "test", ""])
    column = 'test'
    dtype = 'object'
    profiler = TextProfiler(data, column, dtype)
    assert profiler.nan_percantage() == 20.0

def test_patterns():
    """
    
    Test the patterns function of the test profiler
    
    Raises:
    
        - AssertionError: If the patterns found in the data are not as expected.
        
    """
    data = pd.Series(["test", "good", "bad", "test", "good"])
    column = 'test'
    dtype = 'object'
    profiler = TextProfiler(data, column, dtype)
    patterns = profiler.get_patterns()
    expected_patterns = [('AAAA', 4), ('AAA', 1)]
    assert patterns == expected_patterns

def test_profiler_output():
    """
    
    Test the profiler output function of the test profiler
    
    Raises:
    
        - AssertionError: If the profiler output does not contain the expected keys.
        
    """
    data = pd.Series(["test", "good", "bad", "test", "good"])
    column = 'test'
    dtype = 'int'
    profiler = TextProfiler(data, column, dtype)
    profiler_output = profiler.profiler_output()

    expected_keys = {"column", "column_type", "column_length", "mean", "median", "min", "max", \
                     "unique_values", "distinct_values", "nan_percantage", "patterns"}
    assert profiler_output.keys() == expected_keys