from typing import List
import bs4
import requests
from bs4 import BeautifulSoup
from app.utils.error import ServerException


class ScrapingService:
    """
    A service class responsible for handling web scraping tasks
    """

    def __fetch_repository_list(username: str) -> List[bs4.element.Tag]:
        """
        Fetches a list of repository tags from Github for a given github Username

        Args:
            username (str): The Github username whose project data is being scraped

        Returns:
            Tag[]: A list of HTML tags from Github that contain the project data for each repo
        """
        res = requests.get("https://github.com/{}?tab=repositories".format(username))
        soup_data = BeautifulSoup(res.text, "html.parser")
        user_repo_list = soup_data.find(id="user-repositories-list")

        if not user_repo_list:
            raise ServerException("No Github User Page Found", 500)

        repository_list_tags = user_repo_list.find_all("li")

        return repository_list_tags

    def __fetch_repo_description(
        repo_tag: bs4.element.Tag, username: str, repo_name: str
    ) -> str:
        """
        Fetches the decscription of a Repository from Github, given an HTML tag, Github Username, and Repository name
        If the description exceeds 195 characters, an additional request to the specific repository page is made since the
        description will be cutoff on the main user repositories page

        Args:
            repo_tag (str): An HTML tag with information about a repository
            username (str): The Github username whose repo data is being scraped
            repo_name (str): The name of the Github Repository whose description is being fetched

        Returns:
            Tag[]: A list of repo tags from Github that contain the project data
        """
        repo_description_tag = repo_tag.find(attrs={"itemprop": "description"})
        repo_description = ""
        if repo_description_tag:
            repo_description = repo_description_tag.get_text().strip()
            # If repo description is getting cutoff
            if len(repo_description) > 195:
                res = requests.get(
                    "https://github.com/{}/{}".format(username, repo_name)
                )
                repo_data = BeautifulSoup(res.text, "html.parser")
                header = repo_data.find(id="repository-container-header").find(
                    id="responsive-meta-container"
                )
                repo_description_tag = header.find("p")

                if repo_description_tag:
                    repo_description = repo_description_tag.get_text().strip()

    @staticmethod
    def scrape_project_data(username: str):
        """
        Scrape a user's project data from Github given their username

        Args:
            username (str): The Github username whose project data is being scraped

        Returns:
            ProjectData[]: A list of project data from github

        Raises:
            ServerException: Failed to Fetch Project Data from Github
        """
        projects = []
        try:
            repository_list_tags = ScrapingService.__fetch_repository_list(username)
            for repo_tag in repository_list_tags:
                # Repo Name
                repo_name = (
                    repo_tag.find(attrs={"itemprop": "name codeRepository"})
                    .get_text()
                    .strip()
                )

                # Repo Description
                repo_description = ScrapingService.__fetch_repo_description(
                    repo_tag, username, repo_name
                )

                # Repo Stars
                repo_stars_tag = repo_tag.find(
                    attrs={"href": "/{}/{}/stargazers".format(username, repo_name)}
                )
                repo_stars = 0
                if repo_stars_tag:
                    repo_stars = repo_stars_tag.get_text().strip()

                # Repo Forks
                repo_forks_tag = repo_tag.find(
                    attrs={"href": "/{}/{}/forks".format(username, repo_name)}
                )
                repo_forks = 0
                if repo_forks_tag:
                    repo_forks = repo_forks_tag.get_text().strip()

                projects.append(
                    {
                        "repo_name": repo_name,
                        "repo_description": repo_description,
                        "repo_stars": repo_stars,
                        "repo_forks": repo_forks,
                    }
                )

            return projects
        except Exception as e:
            raise ServerException(
                "Failed to Fetch Project Data from Github: {}".format(e), 500
            )
