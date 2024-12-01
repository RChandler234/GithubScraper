from app.services.projects_services import ProjectsService
from app.services.users_services import UsersService
from tests.test_app import MyTest
import json
import uuid
from unittest.mock import patch


class ProjectsMostStarredProjectsControllerTests(MyTest):
    def test_n_greater_than_num_existing_projects(self):
        user = UsersService.create_user("john")
        project = ProjectsService.create_project(
            uuid.UUID(user["id"]), "Project Name", "Project Description", 0, 3
        )

        response = self.client.get("/projects/most-starred/2")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_projects = response_json["projects"]

        assert len(test_projects) == 1

        test_project = test_projects[0]
        assert test_project["user_id"] == user["id"]
        assert test_project["id"] == project["id"]
        assert test_project["name"] == "Project Name"
        assert test_project["description"] == "Project Description"
        assert test_project["forks"] == 0
        assert test_project["stars"] == 3

    def test_no_projects_in_db(self):
        response = self.client.get("/projects/most-starred/2")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_projects = response_json["projects"]

        assert len(test_projects) == 0

    def test_return_in_correct_order(self):
        user = UsersService.create_user("john")
        project_more_stars = ProjectsService.create_project(
            uuid.UUID(user["id"]), "Project More Stars", "Project Description", 0, 3
        )
        project_less_stars = ProjectsService.create_project(
            uuid.UUID(user["id"]), "Project Less Stars", "Project Description", 6, 1
        )

        response = self.client.get("/projects/most-starred/2")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_projects = response_json["projects"]

        assert len(test_projects) == 2
        test_project_more_stars = test_projects[0]
        assert test_project_more_stars["user_id"] == user["id"]
        assert test_project_more_stars["id"] == project_more_stars["id"]
        assert test_project_more_stars["name"] == "Project More Stars"
        assert test_project_more_stars["description"] == "Project Description"
        assert test_project_more_stars["forks"] == 0
        assert test_project_more_stars["stars"] == 3

        test_project_less_stars = test_projects[1]
        assert test_project_less_stars["user_id"] == user["id"]
        assert test_project_less_stars["id"] == project_less_stars["id"]
        assert test_project_less_stars["name"] == "Project Less Stars"
        assert test_project_less_stars["description"] == "Project Description"
        assert test_project_less_stars["forks"] == 6
        assert test_project_less_stars["stars"] == 1

    def test_n_less_than_num_existing_users(self):
        user = UsersService.create_user("john")
        project_more_stars = ProjectsService.create_project(
            uuid.UUID(user["id"]), "Project More Stars", "Project Description", 0, 3
        )
        project_less_stars = ProjectsService.create_project(
            uuid.UUID(user["id"]), "Project Less Stars", "Project Description", 6, 1
        )

        response = self.client.get("/projects/most-starred/1")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_projects = response_json["projects"]

        assert len(test_projects) == 1
        test_project_more_stars = test_projects[0]
        assert test_project_more_stars["user_id"] == user["id"]
        assert test_project_more_stars["id"] == project_more_stars["id"]
        assert test_project_more_stars["name"] == "Project More Stars"
        assert test_project_more_stars["description"] == "Project Description"
        assert test_project_more_stars["forks"] == 0
        assert test_project_more_stars["stars"] == 3

    def test_big_number_users(self):
        user = UsersService.create_user("john")
        project = ProjectsService.create_project(
            uuid.UUID(user["id"]), "Project Name", "Project Description", 0, 3
        )

        response = self.client.get("/projects/most-starred/45")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_projects = response_json["projects"]

        assert len(test_projects) == 1

        test_project = test_projects[0]
        assert test_project["user_id"] == user["id"]
        assert test_project["id"] == project["id"]
        assert test_project["name"] == "Project Name"
        assert test_project["description"] == "Project Description"
        assert test_project["forks"] == 0
        assert test_project["stars"] == 3

    def test_negative_numbers_invalid(self):
        response = self.client.get("/projects/most-starred/-1")
        assert response.status_code == 404

    def test_strings_in_path_invalid(self):
        response = self.client.get("/projects/most-starred/testing")
        assert response.status_code == 404


class ProjectsFetchGithubProjectsByUsernameControllerTests(MyTest):
    def test_username_too_long(self):
        response = self.client.get(
            "/projects/username/adsoijasoijdoiajoijoijoijoijoijjsdoijasodiasdoijoijoijoiijoijojoijoii"
        )
        assert response.status_code == 400

    def test_invalid_character_in_username(self):
        response = self.client.get("/projects/username/testing_")
        assert response.status_code == 400

    def test_projects_do_not_already_exist(self):
        project_data = {
            "repo_name": "Project Name",
            "repo_description": "Project Description",
            "repo_stars": 6,
            "repo_forks": 1,
        }
        project_data_list = [project_data]

        with patch(
            "app.services.scraping_service.ScrapingService.scrape_project_data"
        ) as mock_scrape_data:
            mock_scrape_data.return_value = project_data_list

            response = self.client.get("/projects/username/john")
            assert response.status_code == 200

            response_json = json.loads(response.data.decode("utf-8"))
            test_projects = response_json["projects"]

            assert len(test_projects) == 1

            test_project = test_projects[0]
            assert test_project["username"] == "john"
            assert test_project["name"] == project_data["repo_name"]
            assert test_project["description"] == project_data["repo_description"]
            assert test_project["forks"] == project_data["repo_forks"]
            assert test_project["stars"] == project_data["repo_stars"]

    def test_projects_already_exist_john(self):
        john_user = UsersService.create_user("john")
        ben_user = UsersService.create_user("ben")
        john_project = ProjectsService.create_project(
            uuid.UUID(john_user["id"]), "Project Name", "Project Description", 0, 3
        )
        ben_project = ProjectsService.create_project(
            uuid.UUID(ben_user["id"]),
            "Ben Project Name",
            "Ben Project Description",
            4,
            7,
        )

        response = self.client.get("/projects/username/john")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_projects = response_json["projects"]

        assert len(test_projects) == 1

        test_project = test_projects[0]
        assert test_project["username"] == "john"
        assert test_project["name"] == "Project Name"
        assert test_project["description"] == "Project Description"
        assert test_project["forks"] == 0
        assert test_project["stars"] == 3

    def test_projects_already_exist_ben(self):
        john_user = UsersService.create_user("john")
        ben_user = UsersService.create_user("ben")
        john_project = ProjectsService.create_project(
            uuid.UUID(john_user["id"]), "Project Name", "Project Description", 0, 3
        )
        ben_project = ProjectsService.create_project(
            uuid.UUID(ben_user["id"]),
            "Ben Project Name",
            "Ben Project Description",
            4,
            7,
        )

        response = self.client.get("/projects/username/ben")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_projects = response_json["projects"]

        assert len(test_projects) == 1

        test_project = test_projects[0]
        assert test_project["username"] == "ben"
        assert test_project["name"] == "Ben Project Name"
        assert test_project["description"] == "Ben Project Description"
        assert test_project["forks"] == 4
        assert test_project["stars"] == 7

    def test_multiple_projects_already_exist_john(self):
        john_user = UsersService.create_user("john")
        john_project = ProjectsService.create_project(
            uuid.UUID(john_user["id"]), "Project Name", "Project Description", 0, 3
        )
        other_john_project = ProjectsService.create_project(
            uuid.UUID(john_user["id"]),
            "Other Project Name",
            "Other Project Description",
            4,
            7,
        )

        response = self.client.get("/projects/username/john")
        assert response.status_code == 200

        response_json = json.loads(response.data.decode("utf-8"))
        test_projects = response_json["projects"]

        assert len(test_projects) == 2

        test_project = test_projects[0]
        assert test_project["username"] == "john"
        assert test_project["name"] == "Project Name"
        assert test_project["description"] == "Project Description"
        assert test_project["forks"] == 0
        assert test_project["stars"] == 3

        test_project = test_projects[1]
        assert test_project["username"] == "john"
        assert test_project["name"] == "Other Project Name"
        assert test_project["description"] == "Other Project Description"
        assert test_project["forks"] == 4
        assert test_project["stars"] == 7
