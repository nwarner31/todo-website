from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    # Register Tests
    def test_register_good(self):
        with self.app() as c:
            data = json.dumps({"username": "test", "password": "password"})
            headers = {'content-type': 'application/json'}
            resp = c.post("/register", data=data, headers=headers)

            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.get_data())
            self.assertEqual(data["user"],
                              {"id": 1, "username": "test", "todos": []})

    def test_register_no_username(self):
        with self.app() as c:
            data = json.dumps({"password": "password"})
            headers = {'content-type': 'application/json'}
            resp = c.post("/register", data=data, headers=headers)

            self.assertEqual(resp.status_code, 422)
            message = json.loads(resp.get_data())["errors"]["json"]["username"]
            self.assertEqual(message[0], "Missing data for required field.")

    def test_register_no_password(self):
        with self.app() as c:
            data = json.dumps({"username": "test"})
            headers = {'content-type': 'application/json'}
            resp = c.post("/register", data=data, headers=headers)

            self.assertEqual(resp.status_code, 422)
            message = json.loads(resp.get_data())["errors"]["json"]["password"]
            self.assertEqual(message[0], "Missing data for required field.")

    def test_register_duplicate_username(self):
        with self.app() as c:
            body = json.dumps({"username": "test", "password": "password"})
            headers = {'content-type': 'application/json'}
            resp = c.post("/register", data=body, headers=headers)
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.get_data())
            self.assertEqual(data["user"],
                             {"id": 1, "username": "test", "todos": []})

            resp = c.post("/register", data=body, headers=headers)

            self.assertEqual(resp.status_code, 500)
            self.assertEqual(json.loads(resp.get_data())["status"], "Internal Server Error")

    # Login Tests
    def test_login_good(self):
        with self.app() as c:
            body = json.dumps({"username": "test", "password": "password"})
            headers = {'content-type': 'application/json'}
            c.post("/register", data=body, headers=headers)

            resp = c.post("/login", data=body, headers=headers)

            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.get_data())
            self.assertEqual(data["user"],
                             {"id": 1, "username": "test", "todos": []})

    def test_login_no_username(self):
        with self.app() as c:
            body = json.dumps({"username": "test", "password": "password"})
            headers = {'content-type': 'application/json'}
            c.post("/register", data=body, headers=headers)

            body = json.dumps({"password": "password"})
            resp = c.post("/login", data=body, headers=headers)

            self.assertEqual(resp.status_code, 422)
            message = json.loads(resp.get_data())["errors"]["json"]["username"]
            self.assertEqual(message[0], "Missing data for required field.")

    def test_login_no_password(self):
        with self.app() as c:
            body = json.dumps({"username": "test", "password": "password"})
            headers = {'content-type': 'application/json'}
            c.post("/register", data=body, headers=headers)

            body = json.dumps({"username": "test"})
            resp = c.post("/login", data=body, headers=headers)

            self.assertEqual(resp.status_code, 422)
            message = json.loads(resp.get_data())["errors"]["json"]["password"]
            self.assertEqual(message[0], "Missing data for required field.")

    def test_login_bad_username(self):
        with self.app() as c:
            body = json.dumps({"username": "test", "password": "password"})
            headers = {'content-type': 'application/json'}
            c.post("/register", data=body, headers=headers)

            body = json.dumps({"username": "hello", "password": "password"})
            resp = c.post("/login", data=body, headers=headers)

            self.assertEquals(resp.status_code, 400)
            self.assertEqual(json.loads(resp.get_data())["status"], "Bad Request")

    def test_login_bad_password(self):
        with self.app() as c:
            body = json.dumps({"username": "test", "password": "password"})
            headers = {'content-type': 'application/json'}
            c.post("/register", data=body, headers=headers)

            body = json.dumps({"username": "test", "password": "helloworld"})
            resp = c.post("/login", data=body, headers=headers)

            self.assertEquals(resp.status_code, 400)
            self.assertEqual(json.loads(resp.get_data())["status"], "Bad Request")


