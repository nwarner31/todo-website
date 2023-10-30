from base_test import BaseTest
import json


class TodoTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        with self.app() as c:
            data = json.dumps({"username": "test", "password": "password"})
            headers = {'content-type': 'application/json'}
            resp = c.post("/register", data=data, headers=headers)
            self.token = json.loads(resp.get_data())["token"]

    # Create ToDo - POST /todo
    def test_create_good_both(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            resp = c.post("/todo", data=body, headers=headers)

            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.get_data())
            self.assertEqual(data, {"id": 1, "title": "Test", "is_complete": False})

    def test_create_good_no_complete(self):
        with self.app() as c:
            body = json.dumps({"title": "Test"})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            resp = c.post("/todo", data=body, headers=headers)

            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.get_data())
            self.assertEqual(data, {"id": 1, "title": "Test", "is_complete": False})

    def test_create_no_title(self):
        with self.app() as c:
            body = json.dumps({"is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            resp = c.post("/todo", data=body, headers=headers)

            self.assertEqual(resp.status_code, 422)
            message = json.loads(resp.get_data())["errors"]["json"]["title"]
            self.assertEqual(message[0], "Missing data for required field.")

    def test_create_no_token(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json'}
            resp = c.post("/todo", data=body, headers=headers)

            self.assertEqual(resp.status_code, 401)
            self.assertEqual(json.loads(resp.get_data())["msg"], "Missing Authorization Header")

    def test_create_bad_token(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODY5MzQwNywianRpIjoiNDJlYTI1NGYtOTNiMi00MDM0LWE1ZGEtZWQ5OWEwMzkzMzg5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjk4NjkzNDA3LCJleHAiOjE2OTg2OTQzMDd9.Ew09_AmUL5ELMuLgokhqHn4-HVz0DEX8k7NAVYaSLcc"}
            resp = c.post("/todo", data=body, headers=headers)

            self.assertEqual(resp.status_code, 422)
            self.assertEqual(json.loads(resp.get_data())["msg"], "Signature verification failed")

    # Update ToDo - PUT /todo/<todo.id>
    def test_update_good(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            resp = c.post("/todo", data=body, headers=headers)
            todo_id = json.loads(resp.get_data())["id"]

            body = json.dumps({"title": "Updated", "is_complete": True})

            resp = c.put(f"/todo/{todo_id}", data=body, headers=headers)

            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.get_data())
            self.assertEqual(data, {"id": 1, "title": "Updated", "is_complete": True})

    def test_update_no_title(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            resp = c.post("/todo", data=body, headers=headers)
            todo_id = json.loads(resp.get_data())["id"]

            body = json.dumps({"is_complete": True})

            resp = c.put(f"/todo/{todo_id}", data=body, headers=headers)

            self.assertEqual(resp.status_code, 422)
            message = json.loads(resp.get_data())["errors"]["json"]["title"]
            self.assertEqual(message[0], "Missing data for required field.")

    def test_update_no_complete(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            resp = c.post("/todo", data=body, headers=headers)
            todo_id = json.loads(resp.get_data())["id"]

            body = json.dumps({"title": "Updated"})

            resp = c.put(f"/todo/{todo_id}", data=body, headers=headers)

            self.assertEqual(resp.status_code, 422)
            message = json.loads(resp.get_data())["errors"]["json"]["is_complete"]
            self.assertEqual(message[0], "Missing data for required field.")

    def test_update_no_token(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            resp = c.post("/todo", data=body, headers=headers)
            todo_id = json.loads(resp.get_data())["id"]

            body = json.dumps({"title": "Updated", "is_complete": True})
            headers = {'content-type': 'application/json'}
            resp = c.put(f"/todo/{todo_id}", data=body, headers=headers)

            self.assertEqual(resp.status_code, 401)
            self.assertEqual(json.loads(resp.get_data())["msg"], "Missing Authorization Header")

    def test_update_bad_token(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            resp = c.post("/todo", data=body, headers=headers)
            todo_id = json.loads(resp.get_data())["id"]

            body = json.dumps({"title": "Updated", "is_complete": True})
            headers = {'content-type': 'application/json',
                       "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODY5MzQwNywianRpIjoiNDJlYTI1NGYtOTNiMi00MDM0LWE1ZGEtZWQ5OWEwMzkzMzg5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjk4NjkzNDA3LCJleHAiOjE2OTg2OTQzMDd9.Ew09_AmUL5ELMuLgokhqHn4-HVz0DEX8k7NAVYaSLcc"}
            resp = c.put(f"/todo/{todo_id}", data=body, headers=headers)

            self.assertEqual(resp.status_code, 422)
            self.assertEqual(json.loads(resp.get_data())["msg"], "Signature verification failed")

    def test_update_id_does_not_exist(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            c.post("/todo", data=body, headers=headers)

            body = json.dumps({"title": "Updated", "is_complete": True})

            resp = c.put("/todo/1000", data=body, headers=headers)

            self.assertEqual(resp.status_code, 400)
            self.assertEqual(json.loads(resp.get_data())["status"], "Bad Request")

    def test_update_wrong_user(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            resp = c.post("/todo", data=body, headers=headers)
            todo_id = json.loads(resp.get_data())["id"]

            # register second user to try to update the first user's todo
            data = json.dumps({"username": "user", "password": "password"})
            headers = {'content-type': 'application/json'}
            resp = c.post("/register", data=data, headers=headers)
            token2 = json.loads(resp.get_data())["token"]
            body = json.dumps({"title": "Updated", "is_complete": True})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {token2}"}
            resp = c.put(f"/todo/{todo_id}", data=body, headers=headers)
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(json.loads(resp.get_data())["status"], "Bad Request")

    # Delete ToDo - DELETE /todo/<todo.id>
    def test_delete_good(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            resp = c.post("/todo", data=body, headers=headers)
            todo_id = json.loads(resp.get_data())["id"]

            resp = c.delete(f"/todo/{todo_id}", headers=headers)

            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.get_data())
            self.assertEqual(data, {"code": 200, "message": "ToDo deleted"})

    def test_delete_no_token(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            resp = c.post("/todo", data=body, headers=headers)
            todo_id = json.loads(resp.get_data())["id"]

            headers = {'content-type': 'application/json'}
            resp = c.delete(f"/todo/{todo_id}", headers=headers)

            self.assertEqual(resp.status_code, 401)
            self.assertEqual(json.loads(resp.get_data())["msg"], "Missing Authorization Header")

    def test_delete_bad_token(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            resp = c.post("/todo", data=body, headers=headers)
            todo_id = json.loads(resp.get_data())["id"]

            headers = {'content-type': 'application/json',
                       "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODY5MzQwNywianRpIjoiNDJlYTI1NGYtOTNiMi00MDM0LWE1ZGEtZWQ5OWEwMzkzMzg5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjk4NjkzNDA3LCJleHAiOjE2OTg2OTQzMDd9.Ew09_AmUL5ELMuLgokhqHn4-HVz0DEX8k7NAVYaSLcc"}
            resp = c.delete(f"/todo/{todo_id}", headers=headers)

            self.assertEqual(resp.status_code, 422)
            self.assertEqual(json.loads(resp.get_data())["msg"], "Signature verification failed")

    def test_delete_id_does_not_exist(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            c.post("/todo", data=body, headers=headers)

            resp = c.delete("/todo/1000", headers=headers)

            self.assertEqual(resp.status_code, 400)
            self.assertEqual(json.loads(resp.get_data())["status"], "Bad Request")

    def test_delete_wrong_user(self):
        with self.app() as c:
            body = json.dumps({"title": "Test", "is_complete": False})
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {self.token}"}
            resp = c.post("/todo", data=body, headers=headers)
            todo_id = json.loads(resp.get_data())["id"]

            # register second user to try to update the first user's todo
            data = json.dumps({"username": "user", "password": "password"})
            headers = {'content-type': 'application/json'}
            resp = c.post("/register", data=data, headers=headers)
            token2 = json.loads(resp.get_data())["token"]
            headers = {'content-type': 'application/json',
                       "Authorization": f"Bearer {token2}"}
            resp = c.delete(f"/todo/{todo_id}", headers=headers)
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(json.loads(resp.get_data())["status"], "Bad Request")
