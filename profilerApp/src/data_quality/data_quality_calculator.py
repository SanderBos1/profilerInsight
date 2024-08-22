from src.config import SingletonDB
from src.loaders import DbLoader
from .data_quality_rules import QualityRuleFactory
from src.models import QualityRules, ConnectedTables

DB = SingletonDB.get_instance()

def calculate_data_quality(table_id:str):
        """
        Calculate the data quality score based on the rules and the data.
        """
        rules = QualityRules.query.filter_by(table_id=table_id).all()
        rule_length = len(rules)    
        if rule_length == 0:
            data_quality = 100
        else:
            data_quality = 0
            for rule in rules:
                rule_instance = QualityRuleFactory().create_rule_class(rule.quality_rule)
                data = DbLoader().load(rule.column_name, table_id)[0]
                if rule.extra_info != "":
                    rule_succeded, count = rule_instance.check_rule(rule.threshold, data, rule.extra_info)
                else:
                    rule_succeded, count = rule_instance.check_rule(rule.threshold, data)

                data_quality += rule_succeded
                quality_rule_instance = QualityRules.query.filter_by(rule_id=rule.rule_id).first()
                quality_rule_instance.succeded = rule_succeded
                quality_rule_instance.calculated_threshold = count

            data_quality = data_quality/rule_length * 100
            table = ConnectedTables.query.filter_by(table_id=table_id).first()
            table.data_quality = data_quality
            DB.session.commit()
