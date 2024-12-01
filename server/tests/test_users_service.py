from app.services.users_services import UsersService
from app.utils.error import ServerException
from tests.test_app import MyTest
from app.models import UsersModel, db
from unittest.mock import patch
import time


class UsersCreateUserServiceTests(MyTest):
    def test_username_already_exists(self):
        # Create a user to commit to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session

        with self.assertRaises(ServerException) as context:
            UsersService.create_user("john")

        assert (
            str(context.exception)
            == "Failed to Create User: Username already exists in the database"
        )

    def test_create_project_database_error(self):
        UsersModel.query.filter(UsersModel.username == "john").delete()
        db.session.commit()

        with patch("app.db.session.commit") as mock_commit:
            mock_commit.side_effect = Exception("Simulated database error")

            with self.assertRaises(ServerException) as context:
                UsersService.create_user("john")

            assert (
                str(context.exception)
                == "Failed to Create User: Simulated database error"
            )

            mock_commit.assert_called_once()

            db_user_list = UsersModel.query.filter(UsersModel.username == "john").all()

            assert len(db_user_list) == 0

    def test_create_project_success(self):
        user = UsersService.create_user("john")

        db_user = UsersModel.query.filter(UsersModel.username == "john").first()

        assert db_user.username == "john"


class UsersGetMostRecentUsersServiceTests(MyTest):
    def test_get_users_no_users(self):
        projects = UsersService.get_recent_users(20)
        assert len(projects) == 0

    def test_get_users_database_error(self):
        # Create a user to commit to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session

        with patch("app.models.UsersModel.query") as mock_query:
            mock_query.order_by.return_value.limit.return_value.all.side_effect = (
                Exception("Simulated database error")
            )

            with self.assertRaises(ServerException) as context:
                UsersService.get_recent_users(20)

            assert (
                str(context.exception)
                == "Failed to Fetch Users: Simulated database error"
            )

            mock_query.order_by.return_value.limit.return_value.all.assert_called_once()

    def test_get_users_n_greater_than_num_existing_users(self):
        # Create a user to commit to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        test_user_id = user.id

        users = UsersService.get_recent_users(20)
        assert len(users) == 1
        user = users[0]
        assert user["id"] == str(test_user_id)
        assert user["username"] == "john"

    def test_get_users_success(self):
        # Create a user to commit to the DB
        john_user = UsersModel(username="john")
        db.session.add(john_user)
        db.session.commit()
        assert john_user in db.session
        john_user_id = john_user.id

        time.sleep(1)

        ben_user = UsersModel(username="ben")
        db.session.add(ben_user)
        db.session.commit()
        assert ben_user in db.session
        ben_user_id = ben_user.id

        users = UsersService.get_recent_users(1)

        assert len(users) == 1
        user = users[0]
        assert user["id"] == str(ben_user_id)
        assert user["username"] == "ben"

    def test_get_projects_n_is_0(self):
        # Create a user to commit to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session

        users = UsersService.get_recent_users(0)
        assert len(users) == 0
