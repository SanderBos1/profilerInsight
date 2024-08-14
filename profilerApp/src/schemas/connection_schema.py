from marshmallow import Schema, fields, validate

class ConnectionSchema(Schema):

    "Define the json schema of a database connection."


    connection_id = fields.Str(required=True, validate=validate.Length(min=1))
    host = fields.Str(required=True, validate=validate.Length(min=1))
    port = fields.Str(required=True, validate=validate.Length(min=1))
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=1))
    database = fields.Str(required=True, validate=validate.Length(min=1))
    db_type = fields.Str(required=True, validate=validate.Length(min=1))
