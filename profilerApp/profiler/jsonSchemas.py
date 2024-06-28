from marshmallow import Schema, fields

class getColumnsSchema(Schema):
    tableName = fields.Str(required=True)

class overviewSchema(Schema):
    columName = fields.Str(required=True)