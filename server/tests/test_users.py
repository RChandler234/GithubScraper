from tests.test_app import MyTest
from app.models import UsersModel, db
import json
import time


class MostRecentUsersTest(MyTest):
    def test_n_greater_than_num_existing_users(self):
        # Add a Test User and Doublecheck it was added to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session

        test_user_id = user.id

        response = self.client.get("/users/most-recent/2")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_users = response_json["users"]

        assert len(test_users) == 1

        test_user = test_users[0]
        assert test_user["username"] == "john"
        assert test_user["id"] == str(test_user_id)

    def test_no_users_in_db(self):
        response = self.client.get("/users/most-recent/2")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_users = response_json["users"]

        assert len(test_users) == 0

    def test_return_in_correct_order(self):
        # Add Test Users and Doublecheck they were added to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session

        time.sleep(1)

        test_user_id_john = user.id

        user = UsersModel(username="ben")
        db.session.add(user)
        db.session.commit()
        assert user in db.session

        test_user_id_ben = user.id

        response = self.client.get("/users/most-recent/2")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_users = response_json["users"]

        assert len(test_users) == 2
        test_user_ben = test_users[0]
        assert test_user_ben["username"] == "ben"
        assert test_user_ben["id"] == str(test_user_id_ben)

        test_user_john = test_users[1]
        assert test_user_john["username"] == "john"
        assert test_user_john["id"] == str(test_user_id_john)

    def test_n_less_than_num_existing_users(self):
        # Add Test Users and Doublecheck they were added to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session

        time.sleep(1)

        test_user_id_john = user.id

        user = UsersModel(username="ben")
        db.session.add(user)
        db.session.commit()
        assert user in db.session

        test_user_id_ben = user.id

        response = self.client.get("/users/most-recent/1")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_users = response_json["users"]

        assert len(test_users) == 1
        test_user_ben = test_users[0]
        assert test_user_ben["username"] == "ben"
        assert test_user_ben["id"] == str(test_user_id_ben)

    def test_big_number_users(self):
        # Add a Test User and Doublecheck it was added to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session

        test_user_id = user.id

        response = self.client.get("/users/most-recent/45")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_users = response_json["users"]

        assert len(test_users) == 1

        test_user = test_users[0]
        assert test_user["username"] == "john"
        assert test_user["id"] == str(test_user_id)
