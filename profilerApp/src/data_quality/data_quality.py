from .empty_values_rule import EmptyValuesRule

from src.loaders import DbLoader
from src.models import QualityRules, ConnectedTables
from src.config import SingletonDB  

DB = SingletonDB.get_instance()



class DataQualityRuleGenerator():

    def __init__(self):
        pass

    def get_rule_classes(self):
        
        existing_classes = {
            "No Empty Rule": EmptyValuesRule
        }

        return existing_classes
    
    def get_existing_rules(self):

        rule_descriptions = []
        existing_classes = self.get_rule_classes()
        for rule_class in existing_classes:
            rule_instance = existing_classes[rule_class]()
            rule_description = rule_instance.get_rule_description()
            rule_descriptions.append(rule_description)
        return rule_descriptions

    "needs implementation"
    def calculate_data_quality(self, table_id:str):
        """
        Calculate the data quality score based on the rules and the data.
        """
        rules = QualityRules.query.filter_by(table_id=table_id).all()
        rule_length = len(rules)    
        if rule_length == 0:
            data_quality = 100
        else:
            for rule in rules:
                data_quality = 0
                rule_instance = self.get_rule_classes()[rule.quality_rule]()
                data = DbLoader().load(rule.column_name, table_id)[0]
                rule_succeded, count = rule_instance.check_rule(rule.threshold, data)
                data_quality += rule_succeded
                quality_rule_instance = QualityRules.query.filter_by(rule_id=rule.rule_id).first()
                quality_rule_instance.succeded = rule_succeded
                quality_rule_instance.calculated_threshold = count

            data_quality = data_quality/rule_length
            table = ConnectedTables.query.filter_by(table_id=table_id).first()
            table.data_quality = data_quality
            DB.session.commit()


            