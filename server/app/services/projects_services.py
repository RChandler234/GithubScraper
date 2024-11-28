from app import ProjectsModel, db
from app.transformers.project_transformer import project_transformer
from app.utils.error import ServerException


class ProjectsService:
    """
    A service class responsible for handling interactions with the Project database model
    """

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