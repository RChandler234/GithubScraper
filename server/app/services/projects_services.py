from app.models import ProjectsModel, UsersModel, db
from app.transformers.project_transformer import project_transformer
from app.utils.error import ServerException
from app.services.users_services import UsersService
from app.services.scraping_service import ScrapingService
import uuid


class ProjectsService:
    """
    A service class responsible for handling interactions with the Project Data
    """

    @staticmethod
    def fetch_github_projects_by_username(username: str):
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
            projects = ProjectsService.get_projects_by_username(username)
        except ServerException as e:
            if (not e.message == "Failed to Fetch Projects: Username does not correspond to a user in the database"):
                raise e
            else:
                # If user does not exist in the database, fetch project data from github
                projects_data = ScrapingService.scrape_project_data(username)
                user = UsersService.create_user(username)
                for project in projects_data:
                    created_project = ProjectsService.create_project(
                        uuid.UUID(user.get("id")),
                        project["repo_name"],
                        project["repo_description"],
                        project["repo_forks"],
                        project["repo_stars"],
                    )
                    projects.append(created_project)

        return projects

    @staticmethod
    def get_most_starred_projects(num_projects: int):
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
            projects = (
                ProjectsModel.query.order_by(ProjectsModel.stars.desc())
                .limit(num_projects)
                .all()
            )
            return list(map(project_transformer, projects))
        except Exception as e:
            raise ServerException("Failed to Fetch Projects: {}".format(e), 500)

    @staticmethod
    def create_project(
        user_id: uuid.UUID, name: str, description: str, forks: int, stars: int
    ):
        """
        Create a new project

        Args:
            user_id (UUID): The id of the user to associate the projects with
            name (str): The name of the project
            description (str): The description of the project
            forks (int): The number of forks the project has
            stars (int): The number of stars the project has

        Returns:
            Project: Created Project

        Raises:
            ServerException: Failed to Create Project
            ServerException: Failed to Create Project: User ID does not correspond to a user in the database
        """
        try:
            user = UsersModel.query.filter(UsersModel.id == user_id).first()

            if not user:
                raise ServerException(
                    "User ID does not correspond to a user in the database", 500
                )

            created_project = ProjectsModel(user_id, name, description, forks, stars)
            db.session.add(created_project)
            db.session.commit()
            return project_transformer(created_project)
        except Exception as e:
            db.session.rollback()
            raise ServerException("Failed to Create Project: {}".format(e), 500)

    @staticmethod
    def get_projects_by_username(username: str):
        """
        Gets projects by user username

        Args:
            username (str): The username of the user whose projects are being returned

        Returns:
            Project[]: A list of projects

        Raises:
            ServerException: Failed to Fetch Projects
        """
        try:
            user = UsersModel.query.filter(UsersModel.username == username).first()

            if not user:
                raise ServerException(
                    "Username does not correspond to a user in the database", 500
                )

            projects = ProjectsModel.query.filter(
                ProjectsModel.user_id == user.id
            ).all()
            return list(map(project_transformer, projects))
        except Exception as e:
            raise ServerException("Failed to Fetch Projects: {}".format(e), 500)
