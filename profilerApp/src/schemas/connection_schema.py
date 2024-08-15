from marshmallow import Schema, fields, validate

class ConnectionSchema(Schema):

    "Define the json schema of a database connection."


    connection_id = fields.Str(required=True, validate=validate.Length(min=1))
    server = fields.Str(required=True, validate=validate.Length(min=1))
    port = fields.Int(required=True, validate=validate.Range(min=1, max=65535))
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=1))
    database = fields.Str(required=True, validate=validate.Length(min=1))
    db_type = fields.Str(required=True, validate=validate.Length(min=1))
