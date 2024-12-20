from app.models import UsersModel, db
from app.transformers.user_transformer import user_transformer
from app.utils.error import ServerException


class UsersService:
    """
    A service class responsible for handling interactions with the User Data
    """

    @staticmethod
    def create_user(username: str):
        """
        Gets a user given their username

        Args:
            username (str): The username of the user being created

        Returns:
            User: A user

        Raises:
            ServerException: Failed to Create User
            ServerException: Failed to Create User: Username already exists in the database
        """
        try:
            user = UsersModel.query.filter(UsersModel.username == username).first()

            if user:
                raise ServerException("Username already exists in the database", 500)

            created_user = UsersModel(username=username)
            db.session.add(created_user)
            db.session.commit()
            return user_transformer(created_user)
        except Exception as e:
            db.session.rollback()
            raise ServerException("Failed to Create User: {}".format(e), 500)

    @staticmethod
    def get_recent_users(num_users: int):
        """
        Gets n most recently created users

        Args:
            num_users (int): The number of recent users to fetch

        Returns:
            User[]: A list of users

        Raises:
            ServerException: Failed to Fetch Users
        """
        try:
            users = (
                UsersModel.query.order_by(UsersModel.created_at.desc())
                .limit(num_users)
                .all()
            )
            return list(map(user_transformer, users))
        except Exception as e:
            raise ServerException("Failed to Fetch Users: {}".format(e), 500)
