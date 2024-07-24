from marshmallow import Schema, fields

class csvUploadSchema(Schema):
    csvSeperator = fields.Str(missing=',')
    headerRow = fields.Int(missing=0)
    quoteChar = fields.Str(missing='"')
