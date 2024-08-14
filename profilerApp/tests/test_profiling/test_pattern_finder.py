import pandas as pd

from src.profiling import PatternFinder



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
   