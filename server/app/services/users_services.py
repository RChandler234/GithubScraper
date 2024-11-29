from app.models import UsersModel, db
from app.transformers.user_transformer import user_transformer
from app.utils.error import ServerException

class UsersService:
    """
    A service class responsible for handling interactions with the User database model
    """
    @staticmethod
    def get_user(username):
        try:
            user = UsersModel.query.filter(UsersModel.username == username).first()
            return user_transformer(user)
        except Exception as e:
            raise ServerException("Failed to Fetch User: {}".format(e), 500)
    
    @staticmethod
    def create_user(username):
        try:
            created_user = UsersModel(username=username)
            db.session.add(created_user)
            db.session.commit()
            return user_transformer(created_user)
        except Exception as e:
            raise ServerException("Failed to Create User: {}".format(e), 500)
        
    
    @staticmethod
    def get_recent_users(n):
        try:
            users = UsersModel.query.order_by(UsersModel.created_at.desc()).limit(n)
            return list(map(user_transformer, users))
        except Exception as e:
            raise ServerException("Failed to Fetch Users: {}".format(e), 500)