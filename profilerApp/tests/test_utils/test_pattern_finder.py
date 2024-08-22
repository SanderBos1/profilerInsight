import pandas as pd

from src.utils import PatternFinder



def test_tokenize_string():
    """
    Test the tokenize_string method of the PatternFinder class
    """
    s = "xy67.,@%"
    expected_return = "AA11.,@&"
    pattern_finder = PatternFinder()
    transformed_string = pattern_finder.tokenize_string(s)
    assert expected_return == transformed_string

def test_find_patterns():
    """
    Test the find_patterns method of the PatternFinder class
    """
    input = pd.Series(["xy67.,@%", ""])
    expected_return = [('AA11.,@&', 1), ('', 1)]
    pattern_finder = PatternFinder()
    transformed_string = pattern_finder.find_patterns(input)
    assert expected_return == transformed_string

def test_check_pattern_matches():
    """
    Test the find_patterns method of the PatternFinder class
    """
    input = pd.Series(["1234AB", "1234BC", "1234AB", "1234BC", "1234"])
    expected_return = 1
    pattern_finder = PatternFinder()
    return_count = pattern_finder.check_pattern_matches("1111AA", input)
    assert expected_return == return_count
   