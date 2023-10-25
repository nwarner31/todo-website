import bcrypt
from flask import abort
from flask_smorest import Blueprint
from flask.views import MethodView
from pymysql import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from schemas.user_schemas import UserSchema, UserTokenSchema
from models.users import UserModel
from models.todos import ToDoModel
from blocklist import BLOCKLIST
from db import db
import properties

blp = Blueprint("users", "users", description="user paths")


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, UserTokenSchema)
    def post(self, user_info):
        print(user_info)
        password_bytes = (user_info["password"] + properties.pepper).encode("utf-8")
        try:
            user = UserModel.query.filter(UserModel.username == user_info["username"]).first()
            if user and bcrypt.checkpw(password_bytes, user.password.encode("utf-8")):
                access_token = create_access_token(user.id)
                us = UserTokenSchema()
                us.user = user
                us.token = access_token
                return us
            else:
                abort(400, {"message": "User credentials invalid"})
        except SQLAlchemyError:
            abort(500, {"message": "There was an error"})


@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "You have logged out"}


@blp.route("/register")
class Register(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, UserTokenSchema)
    def post(self, user_info):
        print(user_info)
        password_bytes = (user_info["password"] + properties.pepper).encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        user_info["password"] = hashed_password
        user = UserModel(**user_info)
        try:
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(user.id)
            us = UserTokenSchema()
            us.user = user
            us.token = access_token
            return us
        except IntegrityError:
            abort(499, {"message": "A user with that username already exists"})
        except SQLAlchemyError:
            abort(500, {"message": "An error occurred"})

