import pandas as pd

from src.data_quality import EmptyValuesRule


def test_check_rule():
    """
    Test if the check_rule method returns false when there are empty values in the column.
    """
    empty_values_rule = EmptyValuesRule()
    treshold = 0
    test_df = pd.Series(["1", "test", "3", "", "5"])
    assert empty_values_rule.check_rule(treshold, test_df) == False

def test_check_rule():
    """
    Test if the check_rule method returns true when there are no empty values in the column.
    """
    empty_values_rule = EmptyValuesRule()
    treshold = 0
    test_df = pd.Series(["1", "test", "3", "x", "5"])
    assert empty_values_rule.check_rule(treshold, test_df) == (True, 0.0)
