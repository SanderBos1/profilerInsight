from marshmallow import Schema, fields

class ConnectionSchema(Schema):
    connection_id = fields.Str(required=True)
    host = fields.Str(required=True)
    port = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    database = fields.Str(required=True)
    db_type = fields.Str(required=True)


