from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from schemas.todo_schemas import ToDoSchema, ToDoUpdateSchema
from models.todos import ToDoModel
from db import db

blp = Blueprint("todos", "todos", description="todo paths")


@blp.route("/todo")
class Todos(MethodView):
    @blp.arguments(ToDoSchema)
    @blp.response(200, ToDoSchema)
    @jwt_required()
    def post(self, todo_info):
        user_id = get_jwt()["sub"]
        if user_id:
            try:
                todo = ToDoModel()
                todo.user_id = user_id
                todo.title = todo_info["title"]
                todo.is_complete = todo_info["is_complete"] if "is_complete" in todo_info else False
                db.session.add(todo)
                db.session.commit()
                return todo
            except SQLAlchemyError:
                abort(500, {"message": "There was an error"})
        else:
            abort(400, {"message": "Error authorizing user"})


@blp.route("/todo/<int:todo_id>")
class Todo(MethodView):
    @blp.arguments(ToDoUpdateSchema)
    @blp.response(200, ToDoSchema)
    @jwt_required()
    def put(self, todo_info, todo_id):
        try:
            todo = ToDoModel.query.filter(ToDoModel.id == todo_id).first()
            user_id = get_jwt()["sub"]
            if todo and todo.user_id == user_id:
                todo.title = todo_info["title"]
                todo.is_complete = todo_info["is_complete"]
                db.session.add(todo)
                db.session.commit()
                return todo
            else:
                abort(400, {"message": {"ToDo doesn't exist or it does not belong to you"}})
        except SQLAlchemyError:
            abort(500, {"message": "There was an error"})

    @jwt_required()
    def delete(self, todo_id):
        try:
            user_id = get_jwt()["sub"]
            todo = ToDoModel.query.filter(ToDoModel.id == todo_id).first()
            if todo and todo.user_id == user_id:
                db.session.delete(todo)
                db.session.commit()
                return {"code": 200, "message": "ToDo deleted"}
            else:
                abort(400, {"message": "ToDo doesn't exist or it does not belong to you"})
        except SQLAlchemyError:
            abort(500, {"message": "There was an error"})