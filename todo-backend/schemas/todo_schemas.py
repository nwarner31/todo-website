from marshmallow import Schema, fields


class ToDoSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    is_complete = fields.Bool(default=False)

