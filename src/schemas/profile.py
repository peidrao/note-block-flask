from marshmallow import Schema, fields


class ProfileCreateSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
    created_at = fields.DateTime()


class ProfileSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    username = fields.Str()
    email = fields.Str()
    created_at = fields.DateTime()


class ProfileLoginSchema(Schema):
    username = fields.Str()
    password = fields.Str()
