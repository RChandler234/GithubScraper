from app.services.projects_services import ProjectsService
from app.utils.error import ServerException
from flask_restful import Resource
import re

GITHUB_USERNAME_REGEX = re.compile("^[a-zA-Z0-9-]+$")


class ProjectsGETMostStarredResource(Resource):
    def get(self, num_projects):
        """
        Get n most starred projects
        ---
        parameters:
          - in: path
            name: num_projects
            type: int
            required: true
        responses:
          200:
            description: List of Projects
          400:
            description: Invalid Number of Projects
          500:
            description: Failed to Fetch Projects
        """
        if num_projects < 0:
            raise ServerException(
                "Invalid number of projects, must be a positive number"
            )

        projects = ProjectsService.get_most_starred_projects(num_projects)

        return {"projects": projects}


class ProjectsGETByUsernameResource(Resource):
    def get(self, username):
        """
        Get projects for a given Github Username
        ---
        parameters:
          - in: path
            name: username
            type: string
            required: true
        responses:
          200:
            description: List of Projects
          400:
            description: Invalid Username
          500:
            description: Failed to Get Projects from Github or failed to add or fetch data from the database
        """
        if not GITHUB_USERNAME_REGEX.match(username):
            raise ServerException(
                "Invalid Username. Must only contain alphanumeric characters or -", 400
            )

        if len(username) < 1 or len(username) > 39:
            raise ServerException(
                "Invalid Username. Must be between 1 and 39 characters long", 400
            )

        projects = ProjectsService.get_projects_by_username(username)

        return {"projects": projects}
