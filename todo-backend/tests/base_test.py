from unittest import TestCase
from app import app
from db import db
import properties


class BaseTest(TestCase):
    def setUp(self) -> None:
        app.config["SQLALCHEMY_DATABASE_URI"] = properties.test_db_conn
        with app.app_context():
            if "sqlalchemy" not in app.extensions:
                db.init_app(app)
            db.create_all()
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self) -> None:
        with app.app_context():
            db.session.remove()
            db.drop_all()
