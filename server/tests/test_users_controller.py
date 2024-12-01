from app.services.users_services import UsersService
from tests.test_app import MyTest
import json
import time


class UsersMostRecentUsersControllerTests(MyTest):
    def test_n_greater_than_num_existing_users(self):
        user = UsersService.create_user("john")

        response = self.client.get("/users/most-recent/2")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_users = response_json["users"]

        assert len(test_users) == 1

        test_user = test_users[0]
        assert test_user["username"] == "john"
        assert test_user["id"] == user["id"]

    def test_no_users_in_db(self):
        response = self.client.get("/users/most-recent/2")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_users = response_json["users"]

        assert len(test_users) == 0

    def test_return_in_correct_order(self):
        john_user = UsersService.create_user("john")
        time.sleep(1)
        ben_user = UsersService.create_user("ben")

        response = self.client.get("/users/most-recent/2")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_users = response_json["users"]

        assert len(test_users) == 2
        test_user_ben = test_users[0]
        assert test_user_ben["username"] == "ben"
        assert test_user_ben["id"] == ben_user["id"]

        test_user_john = test_users[1]
        assert test_user_john["username"] == "john"
        assert test_user_john["id"] == john_user["id"]

    def test_n_less_than_num_existing_users(self):
        john_user = UsersService.create_user("john")
        time.sleep(1)
        ben_user = UsersService.create_user("ben")

        response = self.client.get("/users/most-recent/1")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_users = response_json["users"]

        assert len(test_users) == 1
        test_user_ben = test_users[0]
        assert test_user_ben["username"] == "ben"
        assert test_user_ben["id"] == ben_user["id"]

    def test_big_number_users(self):
        john_user = UsersService.create_user("john")

        response = self.client.get("/users/most-recent/45")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_users = response_json["users"]

        assert len(test_users) == 1

        test_user = test_users[0]
        assert test_user["username"] == "john"
        assert test_user["id"] == john_user["id"]

    def test_negative_numbers_invalid(self):
        response = self.client.get("/users/most-recent/-1")
        assert response.status_code == 404

    def test_strings_in_path_invalid(self):
        response = self.client.get("/users/most-recent/testing")
        assert response.status_code == 404
