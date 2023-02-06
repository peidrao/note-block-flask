from marshmallow import Schema, fields


class TagSchema(Schema):
    id = fields.Int()
    tag = fields.Str()
    is_active = fields.Bool()
    created_at = fields.DateTime()
