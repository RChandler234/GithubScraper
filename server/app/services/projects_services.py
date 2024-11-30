from app.models import ProjectsModel, db
from app.transformers.project_transformer import project_transformer
from app.utils.error import ServerException
from app.services.users_services import UsersService
from app.services.scraping_service import ScrapingService


class ProjectsService:
    """
    A service class responsible for handling interactions with the Project Data
    """

    @staticmethod
    def get_projects_by_username(username):
        """
        Gets a profile's Github Projects given their Github Username
        If the user already exists in the database, returns the stored projects
        If the user doesn't exist, scrapes the project data from Github, stores the user and project data in the database,
        and returns the projects

        Args:
            username (str): The username whose projects are being fetched

        Returns:
            Project[]: A list of projects

        Raises:
            ServerException: Failed to Fetch Projects
            ServerException: Failed to Fetch Project Data from Github
            ServerException: Failed to Create User
            ServerException: Failed to Create Project
        """
        projects = []

        try:
            user = UsersService.get_user(username)
            projects = ProjectsService.get_projects_by_user_id(user.get("id"))
        except:
            # If user does not exist in the database, fetch project data from github
            projects_data = ScrapingService.scrape_project_data(username)
            user = UsersService.create_user(username)
            for project in projects_data:
                created_project = ProjectsService.create_project(
                    user.get("id"),
                    project["repo_name"],
                    project["repo_description"],
                    project["repo_forks"],
                    project["repo_stars"],
                )
                projects.append(created_project)

        return projects

    @staticmethod
    def get_most_starred_projects(num_projects):
        """
        Gets n most starred projects from the database

        Args:
            num_projects (int): The number of most starred projects to return

        Returns:
            Project[]: A list of projects

        Raises:
            ServerException: Failed to Fetch Projects
        """
        try:
            projects = ProjectsModel.query.order_by(ProjectsModel.stars.desc()).limit(
                num_projects
            )
            return list(map(project_transformer, projects))
        except Exception as e:
            raise ServerException("Failed to Fetch Project: {}".format(e), 500)

    @staticmethod
    def create_project(user_id, name, description, forks, stars):
        """
        Create a new project

        Args:
            user_id (str): The number of most starred projects to return
            name (str): The name of the project
            description (str): The description of the project
            forks (int): The number of forks the project has
            stars (int): The number of stars the project has

        Returns:
            Project: Created Project

        Raises:
            ServerException: Failed to Create Project
        """
        try:
            created_project = ProjectsModel(user_id, name, description, forks, stars)
            db.session.add(created_project)
            db.session.commit()
            return project_transformer(created_project)
        except Exception as e:
            raise ServerException("Failed to Create Project: {}".format(e), 500)

    @staticmethod
    def get_projects_by_user_id(user_id):
        """
        Gets projects by user id

        Args:
            user_id (str): The id of the user whose projects are being returned

        Returns:
            Project[]: A list of projects

        Raises:
            ServerException: Failed to Fetch Projects
        """
        try:
            projects = ProjectsModel.query.filter(
                ProjectsModel.user_id == user_id
            ).all()
            return list(map(project_transformer, projects))
        except Exception as e:
            raise ServerException("Failed to Fetch Projects: {}".format(e), 500)
