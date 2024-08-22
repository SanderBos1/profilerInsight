from src.data_quality import QualityRuleFactory   
from src.data_quality.empty_values_rule import EmptyValuesRule
from src.data_quality.matching_pattern_rule import PatternRule

def test_get_rule_class():
    """
    Test that the get_rule_classes method returns a dictionary of rule classes.
    """
    data_quality_rule_generator = QualityRuleFactory()
    new_class = data_quality_rule_generator.create_rule_class("No Empty Rule")
    assert isinstance(new_class, EmptyValuesRule)

def test_get_existing_rules():
    """
    Test that the get_existing_rules method returns a list of rule descriptions.
    """
    data_quality_rule_generator = QualityRuleFactory()
    rule_descriptions = data_quality_rule_generator.get_existing_rules()
    rule_descriptions_expected = [ 
        EmptyValuesRule().get_rule_description(), PatternRule().get_rule_description()
    ]
    assert rule_descriptions == rule_descriptions_expected
