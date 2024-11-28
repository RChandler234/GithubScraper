from app import db, UsersModel, ProjectsModel
from app.services.projects_services import ProjectsService
from app.transformers.user_transformer import user_transformer
from app.services.scraping_service import ScrapingService
from app.utils.error import ServerException

class UsersService:
    """
    A service class responsible for handling interactions with the User database model
    """

    @staticmethod
    def find_user_projects(username):
        projects = []

        try:
            user = UsersService.get_user(username)
            projects = ProjectsService.get_projects_by_user_id(user.get("id"))
        except:
            # If user does not exist in the database, fetch project data from github
            projects_data = ScrapingService.scrape_project_data(username)
            user = UsersService.create_user(username)
            for project in projects_data:
                created_project = ProjectsService.create_project(user.get("id"), project["repo_name"], project["repo_description"], project["repo_forks"], project["repo_stars"])
                projects.append(created_project)

        return projects
    
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