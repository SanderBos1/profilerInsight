from marshmallow import Schema, fields

class overviewSchema(Schema):
    tableName = fields.Str(required=True)