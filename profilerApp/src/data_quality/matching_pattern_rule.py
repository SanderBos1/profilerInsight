import pandas as pd

from src.utils import PatternFinder

class PatternRule():

    def __init__(self):
        self.description =  self.set_description()
        self.name = "Match Pattern Rule"

    def check_rule(self , treshold:float, column_data:pd.Series, pattern:str):
        pattern_finder = PatternFinder()
        count = pattern_finder.check_pattern_matches(good_pattern=pattern, data=column_data)
        percentage = count/len(column_data) * 100
        if percentage < treshold:
            return False, percentage
        return True, percentage

    
    def set_description(self):
        description="Calculates the percantage of data points that do not match the input string.\
            If the percantage is higher than the treshold, the rule is not satisfied."
        return description
    
    def get_rule_description(self):
        rule_description = {
            "name": self.name,
            "description": self.description
        }
        return rule_description