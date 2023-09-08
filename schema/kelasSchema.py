from marshmallow import Schema, fields, validate

class KelasSchema(Schema):
    id = fields.String(dump_only=True)
    kelas = fields.String(required=True)
    class Meta:
            strict = True