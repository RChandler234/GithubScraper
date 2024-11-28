import requests
from bs4 import BeautifulSoup
from app.utils.error import ServerException

class ScrapingService:
    """
    A service class responsible for handling web scraping tasks
    """

    def __fetch_repository_list(username):
        res = requests.get('https://github.com/{}?tab=repositories'.format(username))
        soup_data = BeautifulSoup(res.text, 'html.parser')
        user_repo_list = soup_data.find(id="user-repositories-list")

        if (not user_repo_list):
            raise ServerException("No User Github Page Found", 500)
        
        repository_list_tags = user_repo_list.find_all('li')
        
        return repository_list_tags
    
    def __fetch_repo_description(repo_tag, username, repo_name):
        repo_description_tag = repo_tag.find(attrs={'itemprop':"description"})
        repo_description = ''
        if(repo_description_tag):
            repo_description = repo_description_tag.get_text().strip()
            # If repo description is getting cutoff
            if(len(repo_description) > 195):
                res = requests.get('https://github.com/{}/{}'.format(username, repo_name))
                repo_data = BeautifulSoup(res.text, 'html.parser')
                header = repo_data.find(id = 'repository-container-header').find(id="responsive-meta-container")
                repo_description_tag = header.find('p')
                
                if(repo_description_tag):
                    repo_description = repo_description_tag.get_text().strip()
        
    @staticmethod
    def scrape_project_data(username):
        projects = []
        try:
            repository_list_tags = ScrapingService.__fetch_repository_list(username)
            for repo_tag in repository_list_tags:
                # Repo Name
                repo_name = repo_tag.find(attrs={'itemprop': "name codeRepository"}).get_text().strip()

                # Repo Description
                repo_description = ScrapingService.__fetch_repo_description(repo_tag, username, repo_name)

                # Repo Stars
                repo_stars_tag = repo_tag.find(attrs={'href':"/{}/{}/stargazers".format(username, repo_name)})
                repo_stars = 0
                if(repo_stars_tag):
                    repo_stars = repo_stars_tag.get_text().strip()

                # Repo Forks
                repo_forks_tag = repo_tag.find(attrs={'href':"/{}/{}/forks".format(username, repo_name)})
                repo_forks = 0
                if(repo_forks_tag):
                    repo_forks = repo_forks_tag.get_text().strip()

                projects.append({
                    "repo_name": repo_name,
                    "repo_description": repo_description,
                    "repo_stars": repo_stars,
                    "repo_forks": repo_forks
                })
            
            return projects
        except Exception as e:
            raise ServerException('Failed to Fetch Project Data from Github: {}'.format(e), 500)