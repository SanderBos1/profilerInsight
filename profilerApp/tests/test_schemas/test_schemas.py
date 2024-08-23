from marshmallow import ValidationError

from src.schemas import QualityRuleSchema, ConnectionSchema, CSVUploadSchema

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

def test_ConnectionSchema_correct():
    data = {
        "connection_id": "connection_id",
        "server": "server",
        "port": 1,
        "username": "username",
        "password": "password",
        "database": "database",
        "db_type": "db_type"
    }
    schema = ConnectionSchema()
    result = schema.load(data)
    assert result == data

def test_ConnectionSchema_false():
    data = {
        "connection_id": "connection_id",
        "server": "server",
        "port": 1,
        "username": "username",
        "password": "password",
        "database": "database"
    }
    schema = ConnectionSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        result = e.messages
    assert result == {"db_type": ["Missing data for required field."]}

def test_CSVUploadSchema_correct():
    data = {
        "csvSeperator": ",",
        "headerRow": 0,
        "quoteChar": "\""
    }
    schema = CSVUploadSchema()
    result = schema.load(data)
    assert result == data

def test_CSVUploadSchema_false():
    data_incomplete = {
        "csvSeperator": ",",
        "headerRow": 0
    }
    data = {
        "csvSeperator": ",",
        "headerRow": 0,
        "quoteChar": "\""
    }
    schema = CSVUploadSchema()
    result = schema.load(data_incomplete)
    assert result == data