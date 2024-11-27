from flask import Blueprint
from app.services.projects_services import ProjectsService

projects = Blueprint('projects', __name__)

@projects.route('/most-starred/<num_projects>')
def get_most_starred_projects(num_projects):
    # TODO: input validation
    return ProjectsService.get_most_starred_projects(num_projects)
