from marshmallow import Schema, fields

class tableSchema(Schema):
    connectionId = fields.Str(required=True)
    schema = fields.Str(required=True)
    table = fields.Str(required=True)


class deleteTableSchema(Schema):
    schema = fields.Str(required=True)
    table = fields.Str(required=True)



