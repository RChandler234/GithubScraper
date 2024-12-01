from app.services.projects_services import ProjectsService
from app.utils.error import ServerException
from tests.test_app import MyTest
from app.models import ProjectsModel, UsersModel, db
import uuid
from unittest.mock import patch


class ProjectsCreateProjectServiceTests(MyTest):
    def test_create_project_user_not_found(self):
        with self.assertRaises(ServerException) as context:
            ProjectsService.create_project(
                uuid.UUID("5361a11b-615c-42bf-9bdb-e2c3790ada14"),
                "Test Project",
                "A Test Project for Tests",
                0,
                3,
            )

        assert (
            str(context.exception)
            == "Failed to Create Project: User ID does not correspond to a user in the database"
        )

    def test_create_project_database_error(self):
        # Create a user to commit to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        test_user_id = user.id

        with patch("app.db.session.commit") as mock_commit, patch(
            "app.db.session.rollback"
        ) as mock_rollback:
            mock_commit.side_effect = Exception("Simulated database error")

            with self.assertRaises(ServerException) as context:
                ProjectsService.create_project(
                    test_user_id,
                    "Test Project",
                    "A Test Project for Tests",
                    0,
                    3,
                )

            assert (
                str(context.exception)
                == "Failed to Create Project: Simulated database error"
            )

            mock_rollback.assert_called_once()
            mock_commit.assert_called_once()

    def test_create_project_success(self):
        # Create a user to commit to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        test_user_id = user.id

        project = ProjectsService.create_project(
            test_user_id,
            "Test Project",
            "A Test Project for Tests",
            0,
            3,
        )

        db_project = ProjectsModel.query.filter(
            ProjectsModel.id == uuid.UUID(project["id"])
        ).first()

        assert str(db_project.id) == project["id"]
        assert db_project.user_id == test_user_id
        assert db_project.name == "Test Project"
        assert db_project.description == "A Test Project for Tests"
        assert db_project.forks == 0
        assert db_project.stars == 3


class ProjectGetProjectsByUsernameServiceTests(MyTest):
    def test_get_projects_user_not_found(self):
        with self.assertRaises(ServerException) as context:
            ProjectsService.get_projects_by_username("john")

        assert (
            str(context.exception)
            == "Failed to Fetch Projects: Username does not correspond to a user in the database"
        )

    def test_get_projects_database_error(self):
        # Create a user to commit to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        test_user_id = user.id
        created_project = ProjectsModel(test_user_id, "name", "description", 2, 7)
        db.session.add(created_project)
        db.session.commit()
        assert created_project in db.session

        with patch("app.models.ProjectsModel.query") as mock_query:
            mock_query.filter.return_value.all.side_effect = Exception(
                "Simulated database error"
            )

            with self.assertRaises(ServerException) as context:
                ProjectsService.get_projects_by_username("john")

            assert (
                str(context.exception)
                == "Failed to Fetch Projects: Simulated database error"
            )

            mock_query.filter.return_value.all.assert_called_once()

    def test_get_projects_no_projects(self):
        # Create a user to commit to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        projects = ProjectsService.get_projects_by_username("john")

        assert len(projects) == 0

    def test_get_projects_success(self):
        # Create a user to commit to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        test_user_id = user.id
        created_project = ProjectsModel(
            test_user_id, "Project Name", "Project Description", 2, 7
        )
        db.session.add(created_project)
        db.session.commit()
        assert created_project in db.session

        user = UsersModel(username="ben")
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        ben_user_id = user.id
        created_project = ProjectsModel(
            ben_user_id, "Project Name Ben", "Project Description Ben", 4, 1
        )
        db.session.add(created_project)
        db.session.commit()
        assert created_project in db.session

        projects = ProjectsService.get_projects_by_username("john")

        assert len(projects) == 1
        project = projects[0]
        assert project["user_id"] == str(test_user_id)
        assert project["name"] == "Project Name"
        assert project["description"] == "Project Description"
        assert project["forks"] == 2
        assert project["stars"] == 7


class ProjectsGetMostStarredProjectsServiceTests(MyTest):
    def test_get_projects_no_projects(self):
        projects = ProjectsService.get_most_starred_projects(20)
        assert len(projects) == 0

    def test_get_projects_database_error(self):
        # Create a user to commit to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        test_user_id = user.id
        created_project = ProjectsModel(
            test_user_id, "Project Name", "Project Description", 2, 7
        )
        db.session.add(created_project)
        db.session.commit()
        assert created_project in db.session

        with patch("app.models.ProjectsModel.query") as mock_query:
            mock_query.order_by.return_value.limit.return_value.all.side_effect = (
                Exception("Simulated database error")
            )

            with self.assertRaises(ServerException) as context:
                ProjectsService.get_most_starred_projects(20)

            assert (
                str(context.exception)
                == "Failed to Fetch Projects: Simulated database error"
            )

            mock_query.order_by.return_value.limit.return_value.all.assert_called_once()

    def test_get_projects_n_greater_than_num_existing_projects(self):
        # Create a user to commit to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        test_user_id = user.id
        created_project = ProjectsModel(
            test_user_id, "Project Name", "Project Description", 2, 7
        )
        db.session.add(created_project)
        db.session.commit()
        assert created_project in db.session

        projects = ProjectsService.get_most_starred_projects(20)
        assert len(projects) == 1
        project = projects[0]
        assert project["user_id"] == str(test_user_id)
        assert project["name"] == "Project Name"
        assert project["description"] == "Project Description"
        assert project["forks"] == 2
        assert project["stars"] == 7

    def test_get_projects_success(self):
        # Create a user to commit to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        test_user_id = user.id
        created_project = ProjectsModel(
            test_user_id, "Project Name", "Project Description", 6, 1
        )
        db.session.add(created_project)
        db.session.commit()
        assert created_project in db.session
        more_stars_created_project = ProjectsModel(
            test_user_id, "Other Project Name", "Better Project Description", 2, 7
        )
        db.session.add(more_stars_created_project)
        db.session.commit()
        assert more_stars_created_project in db.session

        projects = ProjectsService.get_most_starred_projects(1)
        assert len(projects) == 1
        project = projects[0]
        assert project["user_id"] == str(test_user_id)
        assert project["name"] == "Other Project Name"
        assert project["description"] == "Better Project Description"
        assert project["forks"] == 2
        assert project["stars"] == 7

    def test_get_projects_n_is_0(self):
        # Create a user to commit to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        test_user_id = user.id
        created_project = ProjectsModel(
            test_user_id, "Project Name", "Project Description", 6, 1
        )
        db.session.add(created_project)
        db.session.commit()
        assert created_project in db.session

        projects = ProjectsService.get_most_starred_projects(0)
        assert len(projects) == 0


class ProjectsFetchGithubProjectsByUsername(MyTest):
    def test_projects_already_exist_for_username(self):
        # Create a user to commit to the DB
        user = UsersModel(username="john")
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        test_user_id = user.id
        created_project = ProjectsModel(
            test_user_id, "Project Name", "Project Description", 6, 1
        )
        db.session.add(created_project)
        db.session.commit()
        assert created_project in db.session

        projects = ProjectsService.fetch_github_projects_by_username("john")

        assert len(projects) == 1
        project = projects[0]
        assert project["user_id"] == str(test_user_id)
        assert project["name"] == "Project Name"
        assert project["description"] == "Project Description"
        assert project["forks"] == 6
        assert project["stars"] == 1

    def test_projects_do_not_already_exist_for_username(self):
        project_data = {
            "repo_name": "Project Name",
            "repo_description": "Project Description",
            "repo_stars": 6,
            "repo_forks": 1,
        }
        project_data_list = [project_data]

        with patch(
            "app.services.projects_services.ProjectsService.get_projects_by_username"
        ) as mock_get_projects, patch(
            "app.services.scraping_service.ScrapingService.scrape_project_data"
        ) as mock_scrape_data:
            mock_get_projects.side_effect = ServerException(
                "Failed to Fetch Projects: Username does not correspond to a user in the database"
            )

            mock_scrape_data.return_value = project_data_list
            ProjectsService.fetch_github_projects_by_username("john")

            db_user = UsersModel.query.filter(UsersModel.username == "john").first()

            assert db_user.username == "john"

            db_projects = ProjectsModel.query.filter(
                ProjectsModel.user_id == db_user.id
            ).all()

            assert len(db_projects) == 1
            db_project = db_projects[0]
            assert db_project.user_id == db_user.id
            assert db_project.name == project_data["repo_name"]
            assert db_project.description == project_data["repo_description"]
            assert db_project.forks == project_data["repo_forks"]
            assert db_project.stars == project_data["repo_stars"]
