from flask import Blueprint
from app.services.projects_services import ProjectsService
from app.utils.error import ServerException

projects = Blueprint('projects', __name__)

@projects.route('/most-starred/<int:num_projects>')
def get_most_starred_projects(num_projects):
    if num_projects < 0:
        raise ServerException("Invalid number of users, must be a positive number")
    
    projects = ProjectsService.get_most_starred_projects(num_projects)

    return {"projects": projects}
