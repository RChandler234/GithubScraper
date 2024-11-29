from app.models import ProjectsModel, db
from app.transformers.project_transformer import project_transformer
from app.utils.error import ServerException
from app.services.users_services import UsersService
from app.services.scraping_service import ScrapingService


class ProjectsService:
    """
    A service class responsible for handling interactions with the Project database model
    """
    @staticmethod
    def get_projects_by_username(username):
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
    def get_most_starred_projects(n):
        try:
            projects = ProjectsModel.query.order_by(ProjectsModel.stars.desc()).limit(n)
            return list(map(project_transformer, projects))
        except Exception as e:
            raise ServerException("Failed to Fetch Project: {}".format(e), 500)
    
    @staticmethod
    def create_project(userid, name, description, forks, stars):
        try:
            created_project = ProjectsModel(userid, name, description, forks, stars)
            db.session.add(created_project)
            db.session.commit()
            return project_transformer(created_project)
        except Exception as e:
            raise ServerException("Failed to Create Project: {}".format(e), 500)
    
    @staticmethod
    def get_projects_by_user_id(userid):
        try:
            projects = ProjectsModel.query.filter(ProjectsModel.userid == userid).all()
            return list(map(project_transformer, projects))
        except Exception as e:
            raise ServerException("Failed to Fetch Projects: {}".format(e), 500)