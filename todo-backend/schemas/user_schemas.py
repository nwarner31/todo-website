from marshmallow import Schema, fields

from schemas.todo_schemas import ToDoSchema

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True, required=True)
    todos = fields.List(fields.Nested(ToDoSchema), dump_only=True)


class UserTokenSchema(Schema):
    user = fields.Nested(UserSchema)
    token = fields.Str()
