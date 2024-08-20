from src.data_quality import DataQualityRuleGenerator   
from src.data_quality.empty_values_rule import EmptyValuesRule

def test_get_rule_classes():
    """
    Test that the get_rule_classes method returns a dictionary of rule classes.
    """
    data_quality_rule_generator = DataQualityRuleGenerator()
    existing_classes = data_quality_rule_generator.get_rule_classes()
    existing_classes_expected = {
            "No Empty Rule": EmptyValuesRule
    }
    assert existing_classes == existing_classes_expected

def test_get_existing_rules():
    """
    Test that the get_existing_rules method returns a list of rule descriptions.
    """
    data_quality_rule_generator = DataQualityRuleGenerator()
    rule_descriptions = data_quality_rule_generator.get_existing_rules()
    rule_descriptions_expected = [
        {
            "name": "No Empty Rule",
            "description": "Calculates the percantage of empty values in the column.\
            If the percantage is higher than the treshold, the rule is not satisfied.\
            "
        }
    ]
    assert rule_descriptions == rule_descriptions_expected
