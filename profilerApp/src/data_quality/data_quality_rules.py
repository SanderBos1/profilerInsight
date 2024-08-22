from .empty_values_rule import EmptyValuesRule
from .matching_pattern_rule import PatternRule
from src.config import SingletonDB  

DB = SingletonDB.get_instance()



class QualityRuleFactory():

    def __init__(self):
        pass

    def create_rule_class(self, rule_name:str):
        
        existing_classes = {
            "No Empty Rule": EmptyValuesRule(),
            "Match Pattern Rule": PatternRule()
        }

        return existing_classes[rule_name]
    
    def get_existing_rules(self):

        all_rules = [
            "No Empty Rule",
            "Match Pattern Rule"
        ]

        all_descriptions = []
        for rule in all_rules:
            rule_instance = self.create_rule_class(rule)
            rule_description = rule_instance.get_rule_description()
            all_descriptions.append(rule_description)
        return all_descriptions


            