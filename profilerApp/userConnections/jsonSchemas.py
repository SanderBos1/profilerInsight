from marshmallow import Schema, fields

class ConnectionSchema(Schema):
    connectionId = fields.Str(required=True)
    host = fields.Str(required=True)
    port = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    database = fields.Str(required=True)

class deleteConnectionSchema(Schema):
    connectionId = fields.Str(required=True)

