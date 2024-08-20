from marshmallow import Schema, fields, validate, RAISE

class QualityRuleSchema(Schema):

    "Define the json schema of a data quality rule."
    table_id = fields.Int(required=True, validate=validate.Range(min=1))
    rule_name = fields.Str(required=True, validate=validate.Length(min=1))
    column_name = fields.Str(required=True, validate=validate.Length(min=1))
    threshold = fields.Int(required=True, validate=validate.Range(min=0, max=100))

    class Meta:
        unknown = RAISE

