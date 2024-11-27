from app import ProjectsModel, db
from app.transformers.project_transformer import project_transformer
import requests
from bs4 import BeautifulSoup


class ProjectsService:
    @staticmethod
    def get_most_starred_projects(n):
        projects = ProjectsModel.query.order_by(ProjectsModel.stars.desc()).limit(n)
        results = [project_transformer(project) for project in projects]
        return {"projects": results}
    
    @staticmethod
    def create_project(userid, name, description, forks, stars):
        created_project = ProjectsModel(userid, name, description, forks, stars)
        db.session.add(created_project)
        db.session.commit()
        return project_transformer(created_project)
    
    @staticmethod
    def get_projects_by_user_id(userid):
        projects = ProjectsModel.query.filter(ProjectsModel.userid == userid).all()
        return list(map(project_transformer, projects))
    
    @staticmethod
    def scrape_project_data(username):
        projects = []
        res = requests.get('https://github.com/{}?tab=repositories'.format(username))
        # TODO: handle res.status_code
        soup_data = BeautifulSoup(res.text, 'html.parser')
        repository_list = soup_data.find(id="user-repositories-list").find_all('li')
        for repo in repository_list:
            # Repo Name
            repo_name = repo.find(attrs={'itemprop': "name codeRepository"}).get_text().strip()

            # Repo Description
            repo_description_tag = repo.find(attrs={'itemprop':"description"})
            repo_description = ''
            if(repo_description_tag):
                repo_description = repo_description_tag.get_text().strip()
                # If repo description is getting cutoff
                if(len(repo_description) > 195):
                    res = requests.get('https://github.com/{}/{}'.format(username, repo_name))
                    # TODO: check status code
                    repo_data = BeautifulSoup(res.text, 'html.parser')
                    header = repo_data.find(id = 'repository-container-header').find(id="responsive-meta-container")
                    repo_description_tag = header.find('p')
                    
                    if(repo_description_tag):
                        repo_description = repo_description_tag.get_text().strip()

            # Repo Stars
            repo_stars_tag = repo.find(attrs={'href':"/{}/{}/stargazers".format(username, repo_name)})
            repo_stars = 0
            if(repo_stars_tag):
                repo_stars = repo_stars_tag.get_text().strip()

            # Repo Forks
            repo_forks_tag = repo.find(attrs={'href':"/{}/{}/forks".format(username, repo_name)})
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