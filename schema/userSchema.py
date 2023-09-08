from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    kelas = fields.String(required=True)
    # gender = fields.String(required=False)
    class Meta:
            strict = True