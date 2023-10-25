from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from blueprints.user import blp as user_blueprint
from db import db
import properties

app = Flask(__name__)
cors = CORS(app)

app.config["API_TITLE"] = "ToDo Website API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"

app.config["SQLALCHEMY_DATABASE_URI"] = properties.db_conn
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = properties.jwt_key

db.init_app(app)
with app.app_context():
    db.create_all()

jwt = JWTManager(app)
api = Api(app)

api.register_blueprint(user_blueprint)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, port=5001)
