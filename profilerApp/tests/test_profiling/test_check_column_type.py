import pandas as pd
from src.profiling import CheckType, NumericalProfiler, TextProfiler

def test_check_type_integer():
    """
    Test that the check_type method returns the correct data type when the data is an integer

    Raises:
        - AssertionError: If the type of the data is not as expected 
            and the check_type method does not return the correct data.
    
    """
    int_series = pd.Series([10, 20, 30, 40, 50])
    checker = CheckType(int_series)
    profiler, data, dtype  = checker.check_type()
    assert profiler == NumericalProfiler
    assert data.equals(int_series)

def test_check_type_float():
    """
    Test that the check_type method returns the correct data type when the input is a decimal

    Raises:
        - AssertionError: If the type of the data is not as expected 
            and the check_type method does not return the correct data.
    
    """
    float_series = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    checker = CheckType(float_series)
    profiler, data, dtype  = checker.check_type()
    assert profiler == NumericalProfiler
    assert data.equals(float_series)

def test_check_type_str():
    """
    Test that the check_type method returns the correct data type when the input is a string

    Raises:
        - AssertionError: If the type of the data is not as expected 
            and the check_type method does not return the correct data.
    
    """
    str_series = pd.Series(["test", "test", "test", "test", "test"])
    checker = CheckType(str_series)
    profiler, data, dtype = checker.check_type()
    assert profiler == TextProfiler
    assert data.equals(str_series)

def test_check_type_mixed():
    """
    Test that the check_type method returns the correct data type 
    when the input is a mix of data types

    Raises:
        - AssertionError: If the type of the data is not as expected 
            and the check_type method does not return the correct data.
    
    """
    mixed_series = pd.Series([1, "test", 3, "", 5])
    mixed_series_converted = pd.Series(["1", "test", "3", "", "5"])
    checker = CheckType(mixed_series)
    profiler, data, dtype = checker.check_type()
    assert profiler == TextProfiler
    assert data.equals(mixed_series_converted)