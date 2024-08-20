from marshmallow import ValidationError

from src.schemas import QualityRuleSchema

def test_QualityRuleSchema_correct():
    data = {
        "table_id": 1,
        "rule_name": "rule_name",
        "column_name": "column_name",
        "threshold": 1.0
    }
    schema = QualityRuleSchema()
    result = schema.load(data)
    assert result == data

def test_QualityRuleSchema_false():
    data = {
        "table_id": 1,
        "rule_name": "rule_name",
        "threshold": 1.0
    }
    schema = QualityRuleSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        result = e.messages
    assert result == {"column_name": ["Missing data for required field."]}