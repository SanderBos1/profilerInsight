import pandas as pd

class EmptyValuesRule():

    def __init__(self):
        self.description =  self.set_description()
        self.name = "No Empty Rule"

    def check_rule(self , treshold:float, column_data:pd.Series):
        count_nan = column_data.isna().sum()
        count_empty = (column_data == '').sum()
        sum_empty = float(count_nan + count_empty)
        if sum_empty > treshold:
            return False, sum_empty
        return True, sum_empty
    
    def set_description(self):
        description="Calculates the percantage of empty values in the column.\
            If the percantage is higher than the treshold, the rule is not satisfied.\
            "
        return description
    
    def get_rule_description(self):
        rule_description = {
            "name": self.name,
            "description": self.description
        }
        return rule_description
