from marshmallow import Schema, fields

class tableSchema(Schema):
    uniqueTableName = fields.Str(required=True)
    connectionId = fields.Str(required=True)
    schema = fields.Str(required=True)
    table = fields.Str(required=True)


class deleteTableSchema(Schema):
    uniqueTableName = fields.Str(required=True)



