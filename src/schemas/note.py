from marshmallow import Schema, fields


class NoteSchema(Schema):
    id = fields.Int()
    text = fields.Str()
    profile_id = fields.Int()
    is_active = fields.Bool()
    created_at = fields.DateTime()
