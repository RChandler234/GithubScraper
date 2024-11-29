from app.services.projects_services import ProjectsService
from app.utils.error import ServerException
from flask_restful import Resource
import re

GITHUB_USERNAME_REGEX = re.compile("^[a-zA-Z0-9-]+$")

class ProjectsGETMostStarredResource(Resource):
    def get(self, num_projects):
        if num_projects < 0:
            raise ServerException("Invalid number of users, must be a positive number")
    
        projects = ProjectsService.get_most_starred_projects(num_projects)

        return {"projects": projects}
    
class ProjectsGETByUsernameResource(Resource):
    def get(self, username):
        if not GITHUB_USERNAME_REGEX.match(username):
            raise ServerException( "Invalid Username. Must only contain alphanumeric characters or -", 400)

        if len(username) < 1 or len(username) > 39:
            raise ServerException("Invalid Username. Must be between 1 and 39 characters long", 400)
        
        projects = ProjectsService.get_projects_by_username(username)
        
        return {"projects": projects}