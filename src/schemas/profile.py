from marshmallow import Schema, fields


class ProfileSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    created_at = fields.DateTime()
